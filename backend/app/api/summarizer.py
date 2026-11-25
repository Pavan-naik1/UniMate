from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
from backend.app.services.gemini_service import gemini_service
from backend.app.services.pdf_service import PDFService
from backend.app.database import crud

router = APIRouter(prefix="/summarize", tags=["Summarizer"])

class SummarizeRequest(BaseModel):
    document_id: Optional[str] = None
    custom_text: Optional[str] = None
    summary_type: str = "detailed"  # short, detailed, key_points, definitions, exam_topics, exam_notes, simple_language
    length: str = "medium"          # short, medium, comprehensive

@router.post("")
def generate_summary(req: SummarizeRequest):
    content_to_summarize = ""
    source_name = "Custom Text"
    
    if req.document_id:
        doc = crud.get_document_by_id(req.document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
            
        file_path = doc["file_path"]
        if not Path(file_path).exists():
            raise HTTPException(status_code=404, detail="Document file missing on disk")
            
        pages = PDFService.extract_text_with_pages(file_path)
        content_to_summarize = "\n".join([p["text"] for p in pages])
        source_name = doc["original_name"]
    elif req.custom_text and req.custom_text.strip():
        content_to_summarize = req.custom_text.strip()
    else:
        raise HTTPException(status_code=400, detail="Please provide either a document_id or custom_text to summarize.")
        
    result = gemini_service.summarize_content(
        text_or_context=content_to_summarize,
        summary_type=req.summary_type,
        length=req.length
    )
    
    crud.log_activity(
        action_type="summary_generated",
        description=f"Generated {req.summary_type} summary for {source_name}"
    )
    
    return {
        "summary": result["summary"],
        "summary_type": req.summary_type,
        "source": source_name,
        "engine": result["engine"]
    }
