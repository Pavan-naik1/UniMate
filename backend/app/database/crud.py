import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from backend.app.database.database import get_db_connection

# Document CRUD
def create_document(doc_id: str, filename: str, original_name: str, file_path: str, file_size: int, page_count: int, chunk_count: int = 0) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO documents (id, filename, original_name, file_path, file_size, page_count, chunk_count, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'processed')
    """, (doc_id, filename, original_name, file_path, file_size, page_count, chunk_count))
    conn.commit()
    conn.close()
    return get_document_by_id(doc_id)

def get_documents() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents ORDER BY upload_date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_document_by_id(doc_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_document_db(doc_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# Conversation & Chat CRUD
def create_conversation(title: str = "New Academic Chat") -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    conv_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO conversations (id, title) VALUES (?, ?)", (conv_id, title))
    conn.commit()
    conn.close()
    return {"id": conv_id, "title": title}

def get_conversations() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversations ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_message(conversation_id: str, sender: str, content: str, sources: Optional[List[Dict[str, Any]]] = None, model_used: str = "Gemini-1.5-Flash") -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    msg_id = str(uuid.uuid4())
    sources_json = json.dumps(sources) if sources else None
    
    cursor.execute("""
    INSERT INTO messages (id, conversation_id, sender, content, sources, model_used)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (msg_id, conversation_id, sender, content, sources_json, model_used))
    
    cursor.execute("""
    UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
    """, (conversation_id,))
    
    conn.commit()
    conn.close()
    return {
        "id": msg_id,
        "conversation_id": conversation_id,
        "sender": sender,
        "content": content,
        "sources": sources or [],
        "model_used": model_used
    }

def get_messages(conversation_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC", (conversation_id,))
    rows = cursor.fetchall()
    conn.close()
    result = []
    for row in rows:
        item = dict(row)
        if item.get("sources"):
            try:
                item["sources"] = json.loads(item["sources"])
            except Exception:
                item["sources"] = []
        else:
            item["sources"] = []
        result.append(item)
    return result

def clear_conversation_messages(conversation_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    conn.commit()
    conn.close()

# Quizzes CRUD
def save_quiz(quiz_id: str, title: str, subject: str, document_id: Optional[str], difficulty: str, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO quizzes (id, title, subject, document_id, difficulty, total_questions, score, questions_json)
    VALUES (?, ?, ?, ?, ?, ?, 0, ?)
    """, (quiz_id, title, subject, document_id, difficulty, len(questions), json.dumps(questions)))
    conn.commit()
    conn.close()
    return {"id": quiz_id, "title": title, "subject": subject, "total_questions": len(questions)}

def submit_quiz_answers(quiz_id: str, answers: List[int]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT questions_json FROM quizzes WHERE id = ?", (quiz_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {}
    
    questions = json.loads(row["questions_json"])
    score = 0
    results = []
    for idx, q in enumerate(questions):
        student_ans = answers[idx] if idx < len(answers) else -1
        correct_ans = q.get("correct_answer_index", 0)
        is_correct = (student_ans == correct_ans)
        if is_correct:
            score += 1
        results.append({
            "question": q.get("question"),
            "options": q.get("options", []),
            "student_answer": student_ans,
            "correct_answer": correct_ans,
            "explanation": q.get("explanation", ""),
            "is_correct": is_correct
        })
    
    cursor.execute("""
    UPDATE quizzes 
    SET score = ?, user_answers_json = ?, completed_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (score, json.dumps(results), quiz_id))
    
    conn.commit()
    conn.close()
    return {
        "quiz_id": quiz_id,
        "score": score,
        "total_questions": len(questions),
        "percentage": round((score / len(questions)) * 100, 1) if questions else 0,
        "results": results
    }

def get_quizzes_history() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, subject, difficulty, total_questions, score, created_at, completed_at FROM quizzes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_quiz_details(quiz_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["questions"] = json.loads(data["questions_json"]) if data.get("questions_json") else []
    data["results"] = json.loads(data["user_answers_json"]) if data.get("user_answers_json") else None
    return data

# Study Plans CRUD
def save_study_plan(plan_id: str, subject: str, exam_date: str, daily_hours: float, difficulty: str, topics: List[str], schedule: List[Dict[str, Any]]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO study_plans (id, subject, exam_date, daily_hours, difficulty, topics_json, schedule_json)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (plan_id, subject, exam_date, daily_hours, difficulty, json.dumps(topics), json.dumps(schedule)))
    
    # Insert individual topics into tracking table
    for day_item in schedule:
        day_num = day_item.get("day", 1)
        for topic in day_item.get("topics", []):
            topic_id = str(uuid.uuid4())
            cursor.execute("""
            INSERT INTO study_topics (id, plan_id, topic_name, day, completed)
            VALUES (?, ?, ?, ?, 0)
            """, (topic_id, plan_id, topic, day_num))
            
    conn.commit()
    conn.close()
    return {"id": plan_id, "subject": subject, "schedule": schedule}

def get_all_study_plans() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM study_plans ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    result = []
    for row in rows:
        item = dict(row)
        item["topics"] = json.loads(item["topics_json"]) if item.get("topics_json") else []
        item["schedule"] = json.loads(item["schedule_json"]) if item.get("schedule_json") else []
        result.append(item)
    return result

def get_study_topics_status(plan_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM study_topics WHERE plan_id = ? ORDER BY day ASC", (plan_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def toggle_topic_completion(topic_id: str, completed: bool):
    conn = get_db_connection()
    cursor = conn.cursor()
    completed_val = 1 if completed else 0
    now = datetime.now().isoformat() if completed else None
    cursor.execute("UPDATE study_topics SET completed = ?, completed_at = ? WHERE id = ?", (completed_val, now, topic_id))
    conn.commit()
    conn.close()

# Activity Logging and Analytics
def log_activity(action_type: str, description: str, metadata: Optional[Dict[str, Any]] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO activity_logs (action_type, description, metadata_json)
    VALUES (?, ?, ?)
    """, (action_type, description, json.dumps(metadata) if metadata else None))
    conn.commit()
    conn.close()

def get_recent_activities(limit: int = 10) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activity_logs ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_analytics_metrics() -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total docs
    cursor.execute("SELECT COUNT(*) as count FROM documents")
    total_docs = cursor.fetchone()["count"]
    
    # Total questions / messages
    cursor.execute("SELECT COUNT(*) as count FROM messages WHERE sender = 'user'")
    total_questions = cursor.fetchone()["count"]
    
    # Total quizzes attempted
    cursor.execute("SELECT COUNT(*) as count, AVG(score * 100.0 / total_questions) as avg_score FROM quizzes WHERE completed_at IS NOT NULL")
    quiz_row = cursor.fetchone()
    total_quizzes = quiz_row["count"] or 0
    avg_quiz_score = round(quiz_row["avg_score"] or 0, 1)
    
    # Study topics completion
    cursor.execute("SELECT COUNT(*) as total, SUM(completed) as completed_count FROM study_topics")
    study_row = cursor.fetchone()
    total_topics = study_row["total"] or 0
    completed_topics = study_row["completed_count"] or 0
    study_progress = round((completed_topics / total_topics * 100), 1) if total_topics > 0 else 0
    
    # Quiz scores list for trend chart
    cursor.execute("SELECT title, score, total_questions, (score * 100.0 / total_questions) as percentage, completed_at FROM quizzes WHERE completed_at IS NOT NULL ORDER BY completed_at ASC")
    quiz_scores = [dict(row) for row in cursor.fetchall()]
    
    # Documents breakdown
    cursor.execute("SELECT original_name, page_count, chunk_count, file_size FROM documents ORDER BY upload_date DESC LIMIT 5")
    recent_docs = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return {
        "total_documents": total_docs,
        "total_questions": total_questions,
        "total_quizzes_attempted": total_quizzes,
        "average_quiz_score": avg_quiz_score,
        "total_study_topics": total_topics,
        "completed_study_topics": completed_topics,
        "study_progress_percentage": study_progress,
        "quiz_scores": quiz_scores,
        "recent_documents": recent_docs
    }
