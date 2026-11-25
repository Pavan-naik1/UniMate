import os
import uuid
import shutil
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz  # PyMuPDF

from backend.app.core.config import settings
from backend.app.services.pdf_service import PDFService
from backend.app.rag.vector_store import vector_store
from backend.app.database import crud

router = APIRouter(prefix="/documents", tags=["Documents"])
logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

def safe_unlink(path: Path):
    """Safely unlinks a file, suppressing Windows file lock or non-existent errors."""
    try:
        if path and path.exists():
            path.unlink()
    except Exception as e:
        logger.warning(f"Could not immediately delete file {path}: {e}")

def _process_single_pdf(file: UploadFile) -> Dict[str, Any]:
    """
    Validates, saves, extracts, chunks, embeds, and indexes a single uploaded PDF.
    Guarantees page preservation, duplicate safety, and exact metadata.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename in upload.")
        
    clean_orig_name = Path(file.filename).name
    if not clean_orig_name.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400, 
            detail=f"'{clean_orig_name}' is not a supported file type. Only PDF documents are allowed."
        )

    # Read uploaded bytes into memory for fast validation
    try:
        file_bytes = file.file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read '{clean_orig_name}': {str(e)}")

    file_size = len(file_bytes)
    if file_size == 0:
        raise HTTPException(status_code=400, detail=f"'{clean_orig_name}' is empty (0 bytes). Please upload a valid PDF.")

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"'{clean_orig_name}' exceeds the maximum allowed file size of 25MB.")

    # Validate PDF structure in-memory using PyMuPDF before saving to disk
    try:
        test_doc = fitz.open(stream=file_bytes, filetype="pdf")
        page_count = len(test_doc)
        test_doc.close()
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"'{clean_orig_name}' is corrupted or not a valid readable PDF: {str(e)}"
        )

    if page_count == 0:
        raise HTTPException(status_code=400, detail=f"'{clean_orig_name}' contains zero pages.")

    doc_id = str(uuid.uuid4())
    safe_filename = f"{doc_id}_{clean_orig_name}"
    file_path = settings.UPLOAD_DIR / safe_filename

    # Save validated PDF file to disk
    try:
        with open(file_path, "wb") as f_out:
            f_out.write(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write file '{clean_orig_name}': {str(e)}")

    try:
        # Extract text page by page preserving exact page numbers
        pages_content = PDFService.extract_text_with_pages(str(file_path))
        total_text_len = sum(len(p.get("text", "").strip()) for p in pages_content)
        
        if total_text_len < 10:
            safe_unlink(file_path)
            raise HTTPException(
                status_code=400,
                detail=f"'{clean_orig_name}' contains no readable or extractable text. Please upload a PDF with digital text."
            )

        # Chunk text with overlapping context
        chunks = PDFService.chunk_document(
            pages_content=pages_content,
            doc_id=doc_id,
            doc_name=clean_orig_name
        )

        if not chunks:
            safe_unlink(file_path)
            raise HTTPException(
                status_code=400,
                detail=f"Could not extract meaningful text chunks from '{clean_orig_name}'."
            )

        # Duplicate Safety: Remove any existing version of the document to avoid conflicting chunks
        existing_docs = crud.get_documents()
        for existing in existing_docs:
            if existing["original_name"].lower() == clean_orig_name.lower():
                try:
                    vector_store.delete_document(existing["id"])
                    old_disk_path = Path(existing["file_path"])
                    safe_unlink(old_disk_path)
                    crud.delete_document_db(existing["id"])
                    logger.info(f"Replaced previous duplicate version of '{clean_orig_name}'.")
                except Exception as ex:
                    logger.warning(f"Note during duplicate cleanup of '{clean_orig_name}': {ex}")

        # Index in ChromaDB with Sentence Transformers dense embeddings & metadata
        vector_store.add_chunks(chunks)

        # Record in SQLite database
        doc_record = crud.create_document(
            doc_id=doc_id,
            filename=safe_filename,
            original_name=clean_orig_name,
            file_path=str(file_path),
            file_size=file_size,
            page_count=page_count,
            chunk_count=len(chunks)
        )

        # Log activity for analytics and audit
        crud.log_activity(
            action_type="doc_upload",
            description=f"Uploaded '{clean_orig_name}' ({page_count} pages, {len(chunks)} chunks)",
            metadata={"doc_id": doc_id, "size": file_size, "chunks": len(chunks)}
        )

        return {
            "document": doc_record,
            "chunks_created": len(chunks),
            "filename": clean_orig_name
        }

    except HTTPException:
        raise
    except Exception as e:
        safe_unlink(file_path)
        raise HTTPException(
            status_code=500, 
            detail=f"PDF extraction and indexing failed for '{clean_orig_name}': {str(e)}"
        )


@router.get("/list")
def list_documents():
    """Returns all indexed documents from SQLite."""
    return crud.get_documents()


@router.post("/upload")
async def upload_documents(
    file: Optional[UploadFile] = File(None),
    files: Optional[List[UploadFile]] = File(None)
):
    """
    Accepts single or multiple multipart/form-data PDF uploads.
    """
    upload_list: List[UploadFile] = []
    if files:
        upload_list.extend(files)
    if file:
        upload_list.append(file)

    if not upload_list:
        raise HTTPException(status_code=400, detail="No PDF file was provided for upload.")

    results = []
    total_chunks = 0
    for f in upload_list:
        res = _process_single_pdf(f)
        results.append(res)
        total_chunks += res["chunks_created"]

    if len(results) == 1:
        return {
            "message": f"Successfully uploaded and indexed '{results[0]['filename']}' with {results[0]['chunks_created']} semantic chunks.",
            "document": results[0]["document"],
            "chunks_created": results[0]["chunks_created"],
            "total_documents": 1
        }
    else:
        return {
            "message": f"Successfully uploaded and indexed {len(results)} documents with {total_chunks} total semantic chunks.",
            "documents": [r["document"] for r in results],
            "chunks_created": total_chunks,
            "total_documents": len(results)
        }


@router.post("/upload-multiple")
async def upload_multiple_documents(files: List[UploadFile] = File(...)):
    """
    Batch endpoint for uploading multiple PDF documents simultaneously.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No PDF files provided.")
    results = []
    total_chunks = 0
    for f in files:
        res = _process_single_pdf(f)
        results.append(res)
        total_chunks += res["chunks_created"]

    return {
        "message": f"Successfully uploaded and indexed {len(results)} documents with {total_chunks} total semantic chunks.",
        "documents": [r["document"] for r in results],
        "chunks_created": total_chunks,
        "total_documents": len(results)
    }


@router.delete("/{doc_id}")
def delete_document(doc_id: str):
    """
    Deletes a document from SQLite, removes chunks from ChromaDB, and unlinks file from disk.
    """
    doc = crud.get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    # Delete from ChromaDB
    vector_store.delete_document(doc_id)

    # Delete file from disk
    file_path = Path(doc["file_path"])
    safe_unlink(file_path)

    # Delete from SQLite
    crud.delete_document_db(doc_id)

    crud.log_activity(
        action_type="doc_delete",
        description=f"Deleted document '{doc['original_name']}'"
    )

    return {"message": "Document deleted successfully", "doc_id": doc_id}
