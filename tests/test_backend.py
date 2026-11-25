import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.rag.vector_store import vector_store

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "UniMate" in data["app"]

def test_documents_list_and_sample_seeding():
    response = client.get("/api/documents/list")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) >= 4
    filenames = [d["original_name"] for d in docs]
    assert "GenAI_Study_Notes.pdf" in filenames
    assert "Computer_Science_Syllabus.pdf" in filenames

def test_semantic_vector_retrieval():
    results = vector_store.query("What is self attention and transformer architecture?", n_results=2)
    assert len(results) > 0
    assert "doc_name" in results[0]
    assert "page_number" in results[0]
    assert "similarity" in results[0]
    assert results[0]["similarity"] > 0.0

def test_chat_rag_pipeline():
    response = client.post("/api/chat/message", json={
        "message": "What is the minimum attendance percentage required according to university regulations?",
        "document_id": "all"
    })
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) > 0
    # Check that sources contain citations
    first_source = data["sources"][0]
    assert "document_name" in first_source
    assert "page_number" in first_source

def test_summarizer():
    response = client.post("/api/summarize", json={
        "custom_text": "Generative Artificial Intelligence represents a paradigm shift where deep neural networks generate new synthetic media, text, and computer code using attention mechanisms.",
        "summary_type": "key_points",
        "length": "short"
    })
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert data["summary_type"] == "key_points"

def test_quiz_generator_and_submission():
    # 1. Generate quiz
    gen_response = client.post("/api/quiz/generate", json={
        "topic": "Generative AI and Large Language Models",
        "num_questions": 3,
        "difficulty": "Medium"
    })
    assert gen_response.status_code == 200
    quiz_data = gen_response.json()
    assert "quiz_id" in quiz_data
    assert len(quiz_data["questions"]) == 3
    
    # 2. Submit quiz answers
    sub_response = client.post("/api/quiz/submit", json={
        "quiz_id": quiz_data["quiz_id"],
        "answers": [0, 1, 0]
    })
    assert sub_response.status_code == 200
    sub_data = sub_response.json()
    assert "score" in sub_data
    assert "percentage" in sub_data
    assert len(sub_data["results"]) == 3

def test_study_planner_and_toggle():
    # 1. Generate study plan
    response = client.post("/api/study-planner/generate", json={
        "subject": "Deep Learning & Generative Models",
        "topics": "Transformers, Self-Attention, Vector Stores, Prompt Tuning",
        "daily_hours": 3.0,
        "exam_date": "2026-12-15",
        "difficulty": "Hard"
    })
    assert response.status_code == 200
    plan_data = response.json()
    assert "plan_id" in plan_data
    assert len(plan_data["schedule"]) > 0
    
    # 2. Fetch topics for plan
    topics_res = client.get(f"/api/study-planner/plan/{plan_data['plan_id']}/topics")
    assert topics_res.status_code == 200
    topics_list = topics_res.json()
    assert len(topics_list) > 0
    
    # 3. Toggle completion
    topic_id = topics_list[0]["id"]
    toggle_res = client.post(f"/api/study-planner/topic/{topic_id}/toggle", json={"completed": True})
    assert toggle_res.status_code == 200
    assert toggle_res.json()["completed"] is True

def test_analytics_overview():
    response = client.get("/api/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert data["metrics"]["total_documents"] >= 4
    assert "recent_activities" in data
    assert "quiz_chart_data" in data

def test_genai_concepts_module():
    response = client.get("/api/genai-concepts")
    assert response.status_code == 200
    data = response.json()
    assert "concepts" in data
    assert len(data["concepts"]) == 10
    assert "architecture" in data
