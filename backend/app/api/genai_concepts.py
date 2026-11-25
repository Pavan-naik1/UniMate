from fastapi import APIRouter

router = APIRouter(prefix="/genai-concepts", tags=["GenAI Concepts"])

CONCEPTS = [
    {
        "id": 1,
        "title": "Generative Artificial Intelligence (GenAI)",
        "badge": "Core Paradigm",
        "definition": "A subset of artificial intelligence powered by deep generative models capable of producing new, synthetic content—such as coherent natural language, structured code, diagrams, and multimedia—by learning underlying probability distributions from massive corpora of data.",
        "simple_explanation": "Unlike classical AI that only classifies or predicts labels (e.g., spam vs non-spam), Generative AI can create entirely new answers, lecture summaries, and practice quizzes based on high-level instructions.",
        "real_world_example": "A student asking an AI to synthesize three research papers into a coherent literature review outline.",
        "used_in_unimate": "UniMate uses GenAI to dynamically generate conversational university answers, structured multiple-choice quizzes, exam-oriented notes, and study plans.",
        "code_reference": "backend/app/services/gemini_service.py"
    },
    {
        "id": 2,
        "title": "Large Language Models (LLMs)",
        "badge": "Model Architecture",
        "definition": "Massive deep neural networks based on the Transformer architecture (utilizing multi-head self-attention mechanisms) trained on billions of parameters and extensive textual corpora to predict next-token distributions and perform zero-shot and few-shot reasoning.",
        "simple_explanation": "An LLM acts as an ultra-knowledgeable linguistic reasoning engine that understands complex university questions and responds with fluent, contextually appropriate text.",
        "real_world_example": "Modern conversational systems such as Google Gemini, Claude, and GPT-4.",
        "used_in_unimate": "Acts as the central cognitive engine that synthesizes answers, formats exam questions, and analyzes syllabus requirements.",
        "code_reference": "backend/app/services/gemini_service.py (Gemini 1.5 Flash)"
    },
    {
        "id": 3,
        "title": "Google Gemini",
        "badge": "LLM Provider",
        "definition": "Google's state-of-the-art multimodal foundation model series engineered natively for multimodality, cross-modal reasoning, long-context window processing, and low-latency inference.",
        "simple_explanation": "Gemini provides high-speed, cost-effective, and highly intelligent reasoning capabilities suitable for interactive student chat and rapid educational generation.",
        "real_world_example": "Processing complex technical PDF documents and writing step-by-step mathematical or conceptual derivations.",
        "used_in_unimate": "Integrated via Google Gemini API in backend services to deliver live grounded answers and structured outputs.",
        "code_reference": "backend/app/services/gemini_service.py"
    },
    {
        "id": 4,
        "title": "Prompt Engineering",
        "badge": "Technique",
        "definition": "The methodical discipline of formulating, structuring, and optimizing natural language inputs and system constraints given to an LLM to elicit accurate, truthful, and format-compliant outputs without altering underlying weights.",
        "simple_explanation": "Carefully crafting the prompt given to the AI so it acts strictly as an academic tutor, cites exact pages, prevents hallucination, and returns clean machine-readable JSON for quizzes.",
        "real_world_example": "Directing an AI with role framing: 'You are an accredited university professor; evaluate the following text and return only valid JSON.'",
        "used_in_unimate": "Utilized in UniMate's system prompts to constrain answers strictly to uploaded document excerpts and prevent hallucinated university rules.",
        "code_reference": "backend/app/services/gemini_service.py (generate_rag_answer & generate_quiz)"
    },
    {
        "id": 5,
        "title": "Retrieval-Augmented Generation (RAG)",
        "badge": "Architectural Pattern",
        "definition": "An architectural pattern that optimizes LLM outputs by retrieving authoritative external knowledge chunks from an external vector store at inference time, injecting them into the model's prompt context.",
        "simple_explanation": "Instead of expecting the AI to already memorize your specific college's syllabus or regulations, RAG fetches the exact relevant paragraphs from your uploaded PDF and hands them to the AI to read before answering.",
        "real_world_example": "A university helpdesk answering queries about local 2026 examination timetable rules that were never part of the model's training dataset.",
        "used_in_unimate": "The core backbone of UniMate: ensures all chatbot responses are grounded in actual uploaded PDFs with verified document name and page number citations.",
        "code_reference": "backend/app/rag/vector_store.py & backend/app/api/chat.py"
    },
    {
        "id": 6,
        "title": "Text Embeddings",
        "badge": "Representation",
        "definition": "Dense continuous vector representations of textual sequences generated by transformer encoders, where semantic and syntactic relationships are encoded as geometric distances in multi-hundred-dimensional space.",
        "simple_explanation": "Converting sentences into mathematical vectors (arrays of numbers) such that sentences with similar meanings are close together in Euclidean space, even if they use completely different vocabulary.",
        "real_world_example": "The phrase 'Exam hall admission pass' and 'Student hall ticket' having nearly identical mathematical vector coordinates.",
        "used_in_unimate": "Generated using Sentence Transformers (all-MiniLM-L6-v2) to encode student queries and document chunks.",
        "code_reference": "backend/app/rag/vector_store.py"
    },
    {
        "id": 7,
        "title": "Semantic Search",
        "badge": "Information Retrieval",
        "definition": "A search technique that searches by intent, conceptual contextual meaning, and semantic proximity rather than literal lexical keyword pattern matching.",
        "simple_explanation": "If a student asks 'Can I retake a failed paper?', semantic search finds paragraphs titled 'Supplementary Examination Regulations' even though the exact word 'retake' is not written in the document.",
        "real_world_example": "Modern vector search engines retrieving conceptual matches across scientific research papers.",
        "used_in_unimate": "Executed by querying ChromaDB using cosine similarity across sentence embeddings.",
        "code_reference": "backend/app/rag/vector_store.py (query method)"
    },
    {
        "id": 8,
        "title": "Vector Databases",
        "badge": "Storage & Indexing",
        "definition": "Specialized database management systems designed to index, store, and query high-dimensional vector embeddings using approximate nearest neighbor (ANN) algorithms (e.g., HNSW).",
        "simple_explanation": "A specialized database that holds millions of numerical embeddings and can locate the closest semantic matches to a query vector in milliseconds.",
        "real_world_example": "ChromaDB, Pinecone, Milvus, and Weaviate powering enterprise knowledge assistants.",
        "used_in_unimate": "ChromaDB is embedded with persistent disk storage to store all chunk embeddings permanently across restarts.",
        "code_reference": "backend/app/rag/vector_store.py (ChromaDB PersistentClient)"
    },
    {
        "id": 9,
        "title": "Text Chunking & Sliding Window Overlap",
        "badge": "Data Preprocessing",
        "definition": "The systematic segmentation of long continuous document streams into standardized, semantically coherent passages with bounded character/token lengths and predetermined overlapping boundaries.",
        "simple_explanation": "PDFs are too long to analyze as one block. Chunking cuts them into bite-sized 800-character pieces with 150-character overlaps so sentences split across page boundaries don't lose context.",
        "real_world_example": "Splitting a 50-page university academic handbook into 180 indexed segments with exact page metadata.",
        "used_in_unimate": "Implemented in PDFService using PyMuPDF to extract text with page coordinates and slice with sliding overlap.",
        "code_reference": "backend/app/services/pdf_service.py (chunk_document method)"
    },
    {
        "id": 10,
        "title": "Context-Aware Generation & Grounding",
        "badge": "Generation Safety",
        "definition": "The execution of generative language generation strictly conditioned on supplied reference passages, explicitly restricting the model's factual claims to what is provably supported by the context.",
        "simple_explanation": "Guarantees that the assistant never guesses university policies or fabricates facts; if it's not in the PDF, the AI explicitly states that it could not be found.",
        "real_world_example": "Legal and medical AI assistants that quote specific clauses and refuse to speculate.",
        "used_in_unimate": "Implemented in UniMate's RAG answering prompt with explicit negative constraints and citation mapping.",
        "code_reference": "backend/app/services/gemini_service.py"
    }
]

@router.get("")
def get_genai_concepts():
    return {
        "concepts": CONCEPTS,
        "architecture": {
            "title": "UniMate End-to-End System Architecture",
            "layers": [
                {
                    "name": "Presentation Layer (Frontend)",
                    "technologies": ["React 18", "Vite", "Tailwind CSS", "Lucide React", "Recharts"],
                    "description": "Interactive SaaS dashboard, RAG Chatbot with citation badges, Document Manager, Summarizer, Quiz Engine, Study Planner, and Analytics."
                },
                {
                    "name": "Application & API Layer (Backend)",
                    "technologies": ["FastAPI", "Python 3.10", "Pydantic", "Uvicorn"],
                    "description": "RESTful endpoints for Chat, Documents, Summaries, Quizzes, Study Plans, and SQLite CRUD operations."
                },
                {
                    "name": "Document Ingestion & Processing Pipeline",
                    "technologies": ["PyMuPDF (fitz)", "Sliding Window Chunking", "Regex Cleaning"],
                    "description": "Page-by-page text extraction, metadata extraction, overlapping chunk generation."
                },
                {
                    "name": "Semantic Vector & Embedding Layer",
                    "technologies": ["Sentence Transformers (all-MiniLM-L6-v2)", "ChromaDB Vector Store"],
                    "description": "Dense vector generation, persistent HNSW indexing, cosine similarity nearest-neighbor retrieval."
                },
                {
                    "name": "Generative AI & LLM Cognitive Layer",
                    "technologies": ["Google Gemini 1.5 Flash API", "Structured Prompt Engineering", "Local RAG Fallback"],
                    "description": "Context injection, hallucination prevention, citation attribution, and multi-format academic generation."
                },
                {
                    "name": "Relational Persistence Layer",
                    "technologies": ["SQLite3 (unimate.db)"],
                    "description": "Relational storage of documents, conversations, chat messages, quiz results, study plans, and audit logs."
                }
            ]
        }
    }
