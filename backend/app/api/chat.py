from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.app.database import crud
from backend.app.rag.vector_store import vector_store
from backend.app.rag.doc_resolver import resolve_target_document
from backend.app.services.gemini_service import gemini_service

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    document_id: Optional[str] = None  # None or "all" or specific doc_id

class ConversationCreate(BaseModel):
    title: Optional[str] = "Academic Study Session"

@router.get("/conversations")
def get_conversations():
    return crud.get_conversations()

@router.post("/conversations")
def create_conversation(req: ConversationCreate):
    return crud.create_conversation(title=req.title or "Academic Study Session")

@router.get("/messages/{conversation_id}")
def get_messages(conversation_id: str):
    return crud.get_messages(conversation_id)

@router.post("/message")
def send_chat_message(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    # Get or create conversation
    conv_id = req.conversation_id
    if not conv_id:
        conv = crud.create_conversation(title=req.message[:30] + "...")
        conv_id = conv["id"]
        
    # 1. Save user message to database
    crud.add_message(
        conversation_id=conv_id,
        sender="user",
        content=req.message
    )

    # 2. Resolve document targeting from user message and UI selection
    doc_target = resolve_target_document(
        message=req.message,
        selected_doc_id=req.document_id
    )

    # Case A: User explicitly requested a document that does not exist in uploaded documents
    if doc_target["status"] == "not_found":
        not_found_name = doc_target["requested_name"]
        rag_response = gemini_service.generate_rag_answer(
            question=req.message,
            retrieved_chunks=[],
            is_not_found=True,
            not_found_name=not_found_name
        )
    # Case B: User requested a specific document
    elif doc_target["status"] == "matched":
        retrieved_chunks = vector_store.query(
            query_text=req.message,
            n_results=6,  # Generous context for thorough explanations
            doc_id=doc_target["doc_id"],
            doc_name=doc_target["doc_name"]
        )
        rag_response = gemini_service.generate_rag_answer(
            question=req.message,
            retrieved_chunks=retrieved_chunks,
            target_doc_name=doc_target["doc_name"]
        )
    # Case C: Global search across all uploaded documents
    else:
        retrieved_chunks = vector_store.query(
            query_text=req.message,
            n_results=6,
            doc_id=None,
            doc_name=None
        )
        rag_response = gemini_service.generate_rag_answer(
            question=req.message,
            retrieved_chunks=retrieved_chunks,
            target_doc_name=None
        )
    
    # 3. Save assistant response to database with verified citations
    saved_msg = crud.add_message(
        conversation_id=conv_id,
        sender="assistant",
        content=rag_response["answer"],
        sources=rag_response["sources"],
        model_used=rag_response["engine"]
    )
    
    # 4. Log activity for analytics
    crud.log_activity(
        action_type="chat_query",
        description=f"Asked: '{req.message[:50]}...'",
        metadata={
            "conversation_id": conv_id, 
            "num_sources": len(rag_response["sources"]),
            "target_doc": doc_target.get("doc_name")
        }
    )
    
    return {
        "conversation_id": conv_id,
        "message_id": saved_msg["id"],
        "answer": rag_response["answer"],
        "sources": rag_response["sources"],
        "engine": rag_response["engine"],
        "target_document": doc_target.get("doc_name")
    }

@router.post("/clear/{conversation_id}")
def clear_chat(conversation_id: str):
    crud.clear_conversation_messages(conversation_id)
    return {"status": "cleared", "conversation_id": conversation_id}
