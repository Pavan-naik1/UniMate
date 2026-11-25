import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_query_1_genai_study_notes_only():
    res = client.post("/api/chat/message", json={
        "message": "Explain GenAI_Study_Notes.pdf only.",
        "document_id": "all"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["target_document"] == "GenAI_Study_Notes.pdf"
    assert len(data["sources"]) > 0
    # Every single cited source must be exclusively from GenAI_Study_Notes.pdf
    for s in data["sources"]:
        assert s["document_name"] == "GenAI_Study_Notes.pdf"
        assert s["page_number"] in [1, 2]
    assert "Generative AI" in data["answer"]
    assert "Transformer Architecture" in data["answer"]

def test_query_2_computer_science_syllabus_only():
    res = client.post("/api/chat/message", json={
        "message": "Explain Computer_Science_Syllabus.pdf only.",
        "document_id": "all"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["target_document"] == "Computer_Science_Syllabus.pdf"
    assert len(data["sources"]) > 0
    for s in data["sources"]:
        assert s["document_name"] == "Computer_Science_Syllabus.pdf"
    assert "CS-401" in data["answer"]
    assert "Continuous Internal Evaluation" in data["answer"] or "CIE" in data["answer"]

def test_query_3_university_grading_regulations_only():
    res = client.post("/api/chat/message", json={
        "message": "Explain university grading regulations only.",
        "document_id": "all"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["target_document"] == "University_Academic_Regulations.pdf"
    assert len(data["sources"]) > 0
    for s in data["sources"]:
        assert s["document_name"] == "University_Academic_Regulations.pdf"
    assert "75%" in data["answer"]
    assert "Grading Scale" in data["answer"]

def test_query_4_compare_rag_concepts():
    res = client.post("/api/chat/message", json={
        "message": "Compare RAG concepts from my uploaded documents.",
        "document_id": "all"
    })
    assert res.status_code == 200
    data = res.json()
    assert len(data["sources"]) >= 1
    doc_names = [s["document_name"] for s in data["sources"]]
    assert "GenAI_Study_Notes.pdf" in doc_names or "Computer_Science_Syllabus.pdf" in doc_names
    assert "Retrieval-Augmented Generation" in data["answer"] or "RAG" in data["answer"]

def test_query_5_non_existent_document():
    res = client.post("/api/chat/message", json={
        "message": "Explain Missing_Document_2026.pdf only.",
        "document_id": "all"
    })
    assert res.status_code == 200
    data = res.json()
    assert len(data["sources"]) == 0
    assert "not found" in data["answer"].lower()
