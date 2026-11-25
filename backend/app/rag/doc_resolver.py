import re
from typing import Dict, Any, Optional, List
from pathlib import Path
from backend.app.database import crud

def resolve_target_document(message: str, selected_doc_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyzes student message and UI selection to determine if query targets a specific document.
    
    Returns:
    {
        "status": "matched" | "not_found" | "global",
        "doc_id": Optional[str],
        "doc_name": Optional[str],
        "requested_name": Optional[str]
    }
    """
    documents = crud.get_documents()
    msg_lower = message.lower().strip()
    
    # 1. Check if query asks for a comparison across documents
    # (e.g. "compare ... from my uploaded documents", "across documents")
    comparison_indicators = ["compare", "comparison", "across documents", "from all documents", "my uploaded documents"]
    is_comparison = any(ci in msg_lower for ci in comparison_indicators) and ("only" not in msg_lower)
    if is_comparison and (not selected_doc_id or selected_doc_id == "all"):
        return {
            "status": "global",
            "doc_id": None,
            "doc_name": None,
            "requested_name": None
        }

    # 2. Check for explicit .pdf filename in message
    pdf_matches = re.findall(r'([A-Za-z0-9_\-\.]+\.pdf)', message, re.IGNORECASE)
    if pdf_matches:
        target_file = pdf_matches[0].strip()
        target_lower = target_file.lower()
        
        # Check against available documents in database
        for doc in documents:
            doc_orig = doc["original_name"].lower()
            doc_file = doc["filename"].lower()
            if (target_lower == doc_orig or 
                target_lower == doc_file or 
                target_lower.replace('_', ' ') == doc_orig.replace('_', ' ') or
                Path(target_lower).stem == Path(doc_orig).stem):
                return {
                    "status": "matched",
                    "doc_id": doc["id"],
                    "doc_name": doc["original_name"],
                    "requested_name": target_file
                }
                
        # User requested a specific .pdf that does not exist in uploaded documents
        return {
            "status": "not_found",
            "doc_id": None,
            "doc_name": None,
            "requested_name": target_file
        }

    # 3. Check for natural language document references
    # Define known aliases and keywords for demo documents
    doc_aliases = {
        "GenAI_Study_Notes.pdf": [
            "genai_study_notes", "genai study notes", "genai notes", 
            "generative ai study notes", "generative ai notes"
        ],
        "Computer_Science_Syllabus.pdf": [
            "computer_science_syllabus", "computer science syllabus", 
            "cs syllabus", "cs-401 syllabus", "cs401 syllabus", "cs-401", "cs401"
        ],
        "University_Academic_Regulations.pdf": [
            "university_academic_regulations", "university academic regulations",
            "academic regulations", "university grading regulations", 
            "grading regulations", "attendance regulations"
        ],
        "Examination_Guidelines.pdf": [
            "examination_guidelines", "examination guidelines", "exam guidelines",
            "examination rules", "exam rules", "hall ticket rules", "malpractice policy"
        ]
    }

    # Check known aliases
    for doc in documents:
        doc_name = doc["original_name"]
        aliases = doc_aliases.get(doc_name, [])
        # Add automatic aliases from stem
        stem = Path(doc_name).stem.lower()
        aliases.extend([stem, stem.replace('_', ' ')])
        
        for alias in aliases:
            if alias in msg_lower:
                # Strong match if query says "only", "from [alias]", "in [alias]", or starts with "explain [alias]"
                if ("only" in msg_lower or 
                    f"from {alias}" in msg_lower or 
                    f"in {alias}" in msg_lower or 
                    f"explain {alias}" in msg_lower or
                    f"about {alias}" in msg_lower or
                    f"summarize {alias}" in msg_lower):
                    return {
                        "status": "matched",
                        "doc_id": doc["id"],
                        "doc_name": doc["original_name"],
                        "requested_name": doc["original_name"]
                    }

    # 4. Check UI selector parameter if provided
    if selected_doc_id and selected_doc_id != "all":
        matched_doc = next((d for d in documents if d["id"] == selected_doc_id), None)
        if matched_doc:
            return {
                "status": "matched",
                "doc_id": matched_doc["id"],
                "doc_name": matched_doc["original_name"],
                "requested_name": matched_doc["original_name"]
            }

    # 5. Default to global search across all documents
    return {
        "status": "global",
        "doc_id": None,
        "doc_name": None,
        "requested_name": None
    }
