import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.app.services.gemini_service import gemini_service
from backend.app.services.pdf_service import PDFService
from backend.app.database import crud

router = APIRouter(prefix="/quiz", tags=["Quiz"])

class QuizGenerateRequest(BaseModel):
    document_id: Optional[str] = None
    topic: Optional[str] = None
    num_questions: int = 5
    difficulty: str = "Medium"

class QuizSubmitRequest(BaseModel):
    quiz_id: str
    answers: List[int]

@router.post("/generate")
def generate_quiz(req: QuizGenerateRequest):
    context = ""
    title = req.topic or "University Subject Assessment"
    
    if req.document_id:
        doc = crud.get_document_by_id(req.document_id)
        if doc:
            title = f"Quiz: {doc['original_name']}"
            pages = PDFService.extract_text_with_pages(doc["file_path"])
            context = "\n".join([p["text"] for p in pages[:4]])
            
    if not context and req.topic:
        context = f"Topic: {req.topic}"
        
    if not context:
        context = "Generative AI, Large Language Models, and Retrieval-Augmented Generation concepts."
        
    questions = gemini_service.generate_quiz(
        topic_or_context=context,
        num_questions=req.num_questions,
        difficulty=req.difficulty
    )
    
    quiz_id = str(uuid.uuid4())
    crud.save_quiz(
        quiz_id=quiz_id,
        title=title,
        subject=req.topic or "Computer Science / GenAI",
        document_id=req.document_id,
        difficulty=req.difficulty,
        questions=questions
    )
    
    # Return questions with options for student display
    display_questions = []
    for idx, q in enumerate(questions):
        display_questions.append({
            "index": idx,
            "question": q["question"],
            "options": q["options"]
        })
        
    return {
        "quiz_id": quiz_id,
        "title": title,
        "difficulty": req.difficulty,
        "total_questions": len(display_questions),
        "questions": display_questions
    }

@router.post("/submit")
def submit_quiz(req: QuizSubmitRequest):
    result = crud.submit_quiz_answers(
        quiz_id=req.quiz_id,
        answers=req.answers
    )
    if not result:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    crud.log_activity(
        action_type="quiz_attempt",
        description=f"Completed quiz with score {result['score']}/{result['total_questions']} ({result['percentage']}%)",
        metadata={"quiz_id": req.quiz_id, "score": result["score"]}
    )
    return result

@router.get("/history")
def get_quiz_history():
    return crud.get_quizzes_history()

@router.get("/{quiz_id}")
def get_quiz_details(quiz_id: str):
    quiz = crud.get_quiz_details(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz
