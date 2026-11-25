import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions
from backend.app.core.config import settings

class VectorStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            cls._instance._init_store()
        return cls._instance

    def _init_store(self):
        os.makedirs(str(settings.CHROMA_PERSIST_DIR), exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(settings.CHROMA_PERSIST_DIR),
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Use sentence-transformers all-MiniLM-L6-v2 embeddings
        try:
            self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        except Exception:
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
            
        self.collection = self.client.get_or_create_collection(
            name="unimate_knowledge_base",
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Stores chunk text, metadata, and generates embeddings into ChromaDB.
        Preserves original filename, doc_id, and page_number.
        """
        if not chunks:
            return
            
        ids = [chunk["id"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        
        clean_metadatas = []
        for m in metadatas:
            clean_metadatas.append({
                "doc_id": str(m.get("doc_id", "")),
                "doc_name": str(m.get("doc_name", "")),
                "page_number": int(m.get("page_number", 1)),
                "chunk_index": int(m.get("chunk_index", 0))
            })
            
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=clean_metadatas
        )

    def query(
        self, 
        query_text: str, 
        n_results: int = settings.TOP_K_RESULTS, 
        doc_id: Optional[str] = None,
        doc_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Performs genuine semantic search in ChromaDB.
        Applies strict metadata filtering when doc_id or doc_name is specified.
        Returns top-k matching passages with document name, page number, and similarity score.
        """
        where_filter = None
        if doc_id and doc_id != "all":
            where_filter = {"doc_id": doc_id}
        elif doc_name and doc_name != "all":
            where_filter = {"doc_name": doc_name}
            
        results = self.collection.query(
            query_texts=[query_text],
            n_results=min(n_results, max(1, self.collection.count())),
            where=where_filter
        )
        
        formatted_results = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else []
            distances = results["distances"][0] if "distances" in results and results["distances"] else []
            
            for i, text in enumerate(docs):
                meta = metas[i] if i < len(metas) else {}
                distance = distances[i] if i < len(distances) else 0.0
                similarity = round(max(0.0, 1.0 - distance), 4)
                
                chunk_doc_id = meta.get("doc_id", "")
                chunk_doc_name = meta.get("doc_name", "Unknown Document")
                
                # Strict post-filter check to guarantee zero leakage from other documents
                if doc_id and doc_id != "all" and chunk_doc_id != doc_id:
                    continue
                if doc_name and doc_name != "all" and chunk_doc_name != doc_name:
                    continue
                    
                formatted_results.append({
                    "text": text,
                    "doc_id": chunk_doc_id,
                    "doc_name": chunk_doc_name,
                    "page_number": meta.get("page_number", 1),
                    "similarity": similarity
                })
                
        return formatted_results

    def delete_document(self, doc_id: str):
        """
        Deletes all chunks associated with a document ID from ChromaDB.
        """
        try:
            self.collection.delete(where={"doc_id": doc_id})
        except Exception:
            pass

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_chunks": self.collection.count(),
            "collection_name": self.collection.name
        }

vector_store = VectorStore()
