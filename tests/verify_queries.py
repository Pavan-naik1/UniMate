import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

queries = [
    "Explain GenAI_Study_Notes.pdf only.",
    "Explain Computer_Science_Syllabus.pdf only.",
    "Explain university grading regulations only.",
    "Compare RAG concepts from my uploaded documents.",
    "Explain Non_Existent_File.pdf only."
]

print("\n" + "="*70)
print("RUNNING DOCUMENT-SPECIFIC RETRIEVAL AND ANSWER QUALITY VERIFICATION")
print("="*70)

for idx, q in enumerate(queries, 1):
    print(f"\n--- TEST QUERY {idx}: '{q}' ---")
    res = client.post("/api/chat/message", json={"message": q, "document_id": "all"})
    assert res.status_code == 200, f"Query failed with status {res.status_code}"
    data = res.json()
    
    target_doc = data.get("target_document")
    sources = data.get("sources", [])
    answer = data.get("answer", "")
    
    print(f"Target Document Resolved: {target_doc}")
    print(f"Number of Sources: {len(sources)}")
    
    source_docs = set(s["document_name"] for s in sources)
    print(f"Unique Sourced Documents: {list(source_docs)}")
    
    for s in sources:
        print(f"  [Citation] Doc: {s['document_name']} | Page: {s['page_number']} | Excerpt: {s['excerpt'][:80]}...")
        
    print(f"\nAnswer Output (first 350 chars):\n{answer[:350]}...\n")
    
    # Specific assertions
    if idx == 1:
        assert source_docs == {"GenAI_Study_Notes.pdf"}, f"Expected only GenAI_Study_Notes.pdf, got {source_docs}"
        print("✓ Verified: Query 1 retrieved EXCLUSIVELY from GenAI_Study_Notes.pdf")
    elif idx == 2:
        assert source_docs == {"Computer_Science_Syllabus.pdf"}, f"Expected only Computer_Science_Syllabus.pdf, got {source_docs}"
        print("✓ Verified: Query 2 retrieved EXCLUSIVELY from Computer_Science_Syllabus.pdf")
    elif idx == 3:
        assert source_docs == {"University_Academic_Regulations.pdf"}, f"Expected only University_Academic_Regulations.pdf, got {source_docs}"
        print("✓ Verified: Query 3 retrieved EXCLUSIVELY from University_Academic_Regulations.pdf")
    elif idx == 4:
        assert len(source_docs) >= 1, "Expected at least 1 document for comparison"
        assert "GenAI_Study_Notes.pdf" in source_docs or "Computer_Science_Syllabus.pdf" in source_docs
        print(f"✓ Verified: Query 4 performed comparative synthesis across: {list(source_docs)}")
    elif idx == 5:
        assert len(sources) == 0, f"Expected 0 sources for non-existent document, got {len(sources)}"
        assert "not found" in answer.lower(), "Expected clear not found message"
        print("✓ Verified: Query 5 correctly identified non-existent document with 0 sources")

print("\n" + "="*70)
print("ALL 5 QUERY VERIFICATION TESTS PASSED SUCCESSFULLY!")
print("="*70)
