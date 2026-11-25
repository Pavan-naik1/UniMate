import fitz  # PyMuPDF
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path
from backend.app.core.config import settings

class PDFService:
    @staticmethod
    def extract_text_with_pages(pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extracts text from each page of a PDF using PyMuPDF (fitz).
        Returns a list of dicts: [{"page_number": int, "text": str}]
        """
        doc = fitz.open(pdf_path)
        pages_content = []
        
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            text = page.get_text("text")
            
            # Clean text: remove excessive whitespace and linebreaks
            cleaned_text = re.sub(r'\n+', '\n', text)
            cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text).strip()
            
            pages_content.append({
                "page_number": page_idx + 1,
                "text": cleaned_text
            })
            
        doc.close()
        return pages_content

    @staticmethod
    def chunk_document(
        pages_content: List[Dict[str, Any]], 
        doc_id: str, 
        doc_name: str,
        chunk_size: int = settings.CHUNK_SIZE, 
        chunk_overlap: int = settings.CHUNK_OVERLAP
    ) -> List[Dict[str, Any]]:
        """
        Divides extracted text into overlapping chunks, tracking exact page numbers and document metadata.
        """
        chunks = []
        global_chunk_idx = 0
        
        for page_info in pages_content:
            page_num = page_info["page_number"]
            page_text = page_info["text"]
            
            if not page_text or len(page_text.strip()) < 20:
                continue
                
            start = 0
            text_len = len(page_text)
            
            while start < text_len:
                end = min(start + chunk_size, text_len)
                
                # Try not to cut words in half
                if end < text_len:
                    last_space = page_text.rfind(' ', start, end)
                    if last_space > start + (chunk_size // 2):
                        end = last_space
                        
                chunk_str = page_text[start:end].strip()
                
                if len(chunk_str) >= 20:
                    chunk_id = f"{doc_id}_chunk_{global_chunk_idx}"
                    chunks.append({
                        "id": chunk_id,
                        "text": chunk_str,
                        "metadata": {
                            "doc_id": doc_id,
                            "doc_name": doc_name,
                            "page_number": page_num,
                            "chunk_index": global_chunk_idx,
                            "char_count": len(chunk_str)
                        }
                    })
                    global_chunk_idx += 1
                
                # Move start forward by step
                start = end - chunk_overlap if end - chunk_overlap > start else end
                if start >= text_len:
                    break
                    
        return chunks

    @staticmethod
    def get_pdf_metadata(pdf_path: str) -> Dict[str, Any]:
        """
        Extracts basic metadata (page count, title, author) from PDF.
        """
        doc = fitz.open(pdf_path)
        meta = doc.metadata
        page_count = len(doc)
        doc.close()
        return {
            "page_count": page_count,
            "title": meta.get("title", ""),
            "author": meta.get("author", "")
        }
