import io
import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from backend.app.main import app
from backend.app.database import crud
from backend.app.rag.vector_store import vector_store

client = TestClient(app)

def create_in_memory_pdf(title: str, content: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(title, styles['Title']),
        Spacer(1, 12),
        Paragraph(content, styles['Normal']),
    ]
    doc.build(story)
    buffer.seek(0)
    return buffer.read()

def test_branding_removed_from_frontend_source():
    """Verify that RTD, 30 Marks, and Open Elective do not appear in frontend/src."""
    src_dir = Path("frontend/src")
    forbidden_terms = ["RTD Open Elective", "30 Marks", "Open Elective"]
    
    found_matches = []
    for f in src_dir.rglob("*.jsx"):
        text = f.read_text(encoding="utf-8")
        for term in forbidden_terms:
            if term.lower() in text.lower():
                found_matches.append(f"{f.name}: {term}")

    assert len(found_matches) == 0, f"Found forbidden branding in frontend: {found_matches}"

def test_branding_removed_from_sidebar_card():
    """Verify AI Engine card has Local RAG and Sentence Transformers + ChromaDB in MainLayout.jsx."""
    layout_file = Path("frontend/src/layouts/MainLayout.jsx")
    text = layout_file.read_text(encoding="utf-8")
    assert "AI ENGINE" in text
    assert "Sentence Transformers + ChromaDB" in text
    assert "RTD" not in text

def test_upload_invalid_file_type():
    """Non-PDF files must be rejected with 400 Bad Request."""
    response = client.post(
        "/api/documents/upload",
        files={"file": ("invalid.txt", b"This is a text file", "text/plain")}
    )
    assert response.status_code == 400
    assert "Only PDF documents are allowed" in response.json()["detail"] or "not a supported file type" in response.json()["detail"]

def test_upload_empty_pdf():
    """Empty 0-byte PDFs must be rejected with 400 Bad Request."""
    response = client.post(
        "/api/documents/upload",
        files={"file": ("empty.pdf", b"", "application/pdf")}
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

def test_upload_corrupt_pdf():
    """Corrupted PDF bytes must be rejected with 400 Bad Request."""
    response = client.post(
        "/api/documents/upload",
        files={"file": ("corrupt.pdf", b"%PDF-1.4 corrupted binary junk...", "application/pdf")}
    )
    assert response.status_code == 400
    assert "corrupted" in response.json()["detail"].lower() or "not a valid readable pdf" in response.json()["detail"].lower()

def test_upload_valid_pdf_and_rag_query():
    """Test full pipeline: upload custom PDF, extract text, embed in ChromaDB, query in Chatbot."""
    pdf_name = "Machine_Learning_SVM_Guide.pdf"
    pdf_content = (
        "Support Vector Machines (SVM) are supervised learning models with associated learning algorithms "
        "that analyze data for classification and regression analysis. Given a set of training examples, "
        "each marked as belonging to one of two categories, an SVM training algorithm builds a model that "
        "assigns new examples to one category or the other, making it a non-probabilistic binary linear classifier. "
        "An SVM maps training examples to points in space so as to maximize the width of the gap between the two categories. "
        "New examples are then mapped into that same space and predicted to belong to a category based on which side of the gap they fall on."
    )
    pdf_bytes = create_in_memory_pdf("Machine Learning: Support Vector Machines", pdf_content)

    # 1. Upload
    response = client.post(
        "/api/documents/upload",
        files={"file": (pdf_name, pdf_bytes, "application/pdf")}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["chunks_created"] > 0
    assert data["document"]["original_name"] == pdf_name
    doc_id = data["document"]["id"]

    # 2. Check appearance in documents list
    list_res = client.get("/api/documents/list")
    assert list_res.status_code == 200
    docs = list_res.json()
    assert any(d["id"] == doc_id for d in docs)
    uploaded_doc = next(d for d in docs if d["id"] == doc_id)
    assert uploaded_doc["original_name"] == pdf_name
    assert uploaded_doc["upload_date"] is not None
    assert uploaded_doc["status"] == "processed"

    # 3. Query Chatbot specifically for this document
    chat_res = client.post("/api/chat/message", json={
        "message": f"Explain {pdf_name} only."
    })
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert chat_data["target_document"] == pdf_name
    assert len(chat_data["sources"]) > 0
    for s in chat_data["sources"]:
        assert s["document_name"] == pdf_name
        assert s["page_number"] >= 1
    assert "Support Vector Machines" in chat_data["answer"] or "SVM" in chat_data["answer"]

    # 4. Test safe duplicate upload (re-uploading same filename)
    updated_bytes = create_in_memory_pdf("Machine Learning: Updated SVM", pdf_content + " Soft-margin relaxation allows misclassifications.")
    dup_res = client.post(
        "/api/documents/upload",
        files={"file": (pdf_name, updated_bytes, "application/pdf")}
    )
    assert dup_res.status_code == 200
    dup_data = dup_res.json()
    assert dup_data["document"]["original_name"] == pdf_name
    new_doc_id = dup_data["document"]["id"]

    # Verify old doc_id is replaced
    post_dup_docs = client.get("/api/documents/list").json()
    matching_docs = [d for d in post_dup_docs if d["original_name"] == pdf_name]
    assert len(matching_docs) == 1
    assert matching_docs[0]["id"] == new_doc_id

    # 5. Clean up uploaded test document
    del_res = client.delete(f"/api/documents/{new_doc_id}")
    assert del_res.status_code == 200

def test_batch_pdf_upload():
    """Test uploading multiple PDFs in a single request."""
    pdf1_bytes = create_in_memory_pdf("Batch Document One", "First batch test document contents for indexing.")
    pdf2_bytes = create_in_memory_pdf("Batch Document Two", "Second batch test document contents for indexing.")

    response = client.post(
        "/api/documents/upload-multiple",
        files=[
            ("files", ("Batch_One.pdf", pdf1_bytes, "application/pdf")),
            ("files", ("Batch_Two.pdf", pdf2_bytes, "application/pdf"))
        ]
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["total_documents"] == 2
    assert len(data["documents"]) == 2

    # Clean up batch test documents
    for doc in data["documents"]:
        client.delete(f"/api/documents/{doc['id']}")
