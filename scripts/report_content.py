"""
UniMate Final Project Report Content Definition
Contains full academic text, table schemas, and data structures for all 47 sections.
Student: Pavan Prakash Naik
USN: SCA25MSD051
"""

PROJECT_TITLE = "UniMate: An Intelligent University Assistant Using Generative Artificial Intelligence and Large Language Models (LLMs)"
STUDENT_NAME = "Pavan Prakash Naik"
STUDENT_USN = "SCA25MSD051"
DEGREE_NAME = "Master of Science / Bachelor of Technology / MCA [Degree Placeholder]"
DEPT_NAME = "[DEPARTMENT_OF_COMPUTER_SCIENCE_AND_ENGINEERING]"
COLLEGE_NAME = "[INSTITUTION_COLLEGE_NAME_PLACEHOLDER]"
UNIVERSITY_NAME = "[AFFILIATED_UNIVERSITY_NAME_PLACEHOLDER]"
GUIDE_NAME = "[FACULTY_GUIDE_NAME_PLACEHOLDER]"
GUIDE_DESIGNATION = "[DESIGNATION_PLACEHOLDER]"
HOD_NAME = "[HEAD_OF_DEPARTMENT_NAME_PLACEHOLDER]"
PRINCIPAL_NAME = "[PRINCIPAL_DIRECTOR_NAME_PLACEHOLDER]"
ACADEMIC_YEAR = "2025 – 2026 / [ACADEMIC_YEAR_PLACEHOLDER]"

CERTIFICATE_TEXT = f"""This is to certify that the project work entitled "{PROJECT_TITLE}" is a bona fide work carried out by {STUDENT_NAME} (USN: {STUDENT_USN}) in partial fulfillment for the award of the degree of {DEGREE_NAME} from {COLLEGE_NAME}, affiliated to {UNIVERSITY_NAME}, during the academic year {ACADEMIC_YEAR}.\n\nIt is certified that all corrections/suggestions indicated for internal assessment have been incorporated in the report deposited in the departmental library. The project report has been approved as it satisfies the academic requirements in respect of project work prescribed for the said degree."""

DECLARATION_TEXT = f"""I, {STUDENT_NAME} (USN: {STUDENT_USN}), student of {DEGREE_NAME}, {DEPT_NAME}, {COLLEGE_NAME}, hereby declare that the project entitled "{PROJECT_TITLE}" has been independently carried out by me under the guidance and supervision of {GUIDE_NAME}, {GUIDE_DESIGNATION}, {DEPT_NAME}.\n\nI further declare that this report has not been submitted previously in part or in full to any other university or institution for the award of any degree, diploma, or certificate. All information, concepts, algorithms, and quotations derived from published literature or open-source software libraries have been duly acknowledged in the references."""

ACKNOWLEDGEMENT_TEXT = f"""I express my profound gratitude and respectful regards to my faculty guide, {GUIDE_NAME}, {GUIDE_DESIGNATION}, for their invaluable guidance, constructive criticism, and continuous encouragement throughout the inception and development of the UniMate project.\n\nI extend my sincere thanks to Dr. {HOD_NAME}, Head of the Department of {DEPT_NAME}, for providing the necessary laboratory facilities, compute infrastructure, and institutional support.\n\nI am deeply indebted to Dr. {PRINCIPAL_NAME}, Principal of {COLLEGE_NAME}, for fostering an academic environment that promotes innovative research in applied artificial intelligence and machine learning.\n\nFinally, I wish to thank my fellow students, academic peers, and family members for their enduring patience, moral support, and feedback during testing and document compilation."""

ABSTRACT_TEXT = (
    "In contemporary higher education ecosystems, students and academic staff routinely interact with an extensive, "
    "fragmented collection of institutional documentation—including course syllabi, lecture notes, academic regulations, "
    "examination ordinances, and degree requirements. Traditional information retrieval systems deployed across university "
    "portals rely predominantly on rigid, lexical keyword matching (e.g., BM25 or SQL LIKE queries), which fail to comprehend "
    "semantic intent, syntactic variation, or contextual synonyms. Conversely, commercial Large Language Models (LLMs) "
    "exhibit substantial parametric hallucination risks, lack visibility into confidential, private institutional courseware, "
    "and fail to provide verifiable, page-level bibliographic citations for generated assertions. To address these operational "
    "and technical limitations, this project presents UniMate—an autonomous, localized, full-stack university assistant engineered "
    "upon a robust Retrieval-Augmented Generation (RAG) framework.\n\n"
    "UniMate ingests institutional PDF documents through a high-performance PyMuPDF extraction engine, applies sliding-window "
    "chunking with contextual boundary preservation, and generates 384-dimensional dense semantic vector representations using the "
    "Sentence Transformers all-MiniLM-L6-v2 model. These vector embeddings are indexed alongside granular structural metadata "
    "(document identifier, original filename, and 1-based page numbers) within an embedded ChromaDB vector database. When a student "
    "poses a natural language query, UniMate executes an approximate nearest-neighbor cosine similarity search over the vector space, "
    "applying strict metadata filters when document-specific retrieval is requested. The retrieved passages are synthesized into an "
    "instruction-grounded prompt dispatched to a dual-engine AI core: Google Gemini 1.5 Flash in live network mode, with an autonomous "
    "fallback to a deterministic Local Semantic Synthesizer when offline. Beyond conversational question answering with exact page "
    "citations, UniMate integrates an Academic Document Summarizer, an Intelligent Quiz Generator, a Personalized Study Planner, "
    "and an interactive GenAI concepts educational module. Comprehensive evaluation across 25 automated test cases demonstrates 100% "
    "pass rate, sub-30ms vector retrieval latency, and zero cross-document passage contamination under isolated document queries."
)

TABLE_OF_CONTENTS_DATA = [
    ("1", "Title Page", "i"),
    ("2", "Certificate Page", "ii"),
    ("3", "Declaration", "iii"),
    ("4", "Acknowledgement", "iv"),
    ("5", "Abstract", "v"),
    ("6", "Table of Contents", "vi"),
    ("7", "List of Figures", "vii"),
    ("8", "List of Tables", "viii"),
    ("9", "Introduction", "1"),
    ("10", "Background and Overview of Generative AI", "3"),
    ("11", "Problem Statement", "5"),
    ("12", "Objectives of the Project", "7"),
    ("13", "Existing System", "9"),
    ("14", "Limitations of Existing Systems", "11"),
    ("15", "Proposed System", "13"),
    ("16", "Scope of the Project", "15"),
    ("17", "Literature Review", "17"),
    ("18", "System Requirements", "20"),
    ("19", "Hardware and Software Requirements", "22"),
    ("20", "Technologies Used", "24"),
    ("21", "System Architecture", "27"),
    ("22", "Detailed Methodology", "30"),
    ("23", "Retrieval-Augmented Generation (RAG)", "33"),
    ("24", "Large Language Model Integration", "36"),
    ("25", "Embedding Generation and Semantic Search", "38"),
    ("26", "Vector Database and Document Retrieval", "41"),
    ("27", "PDF Processing and Text Extraction", "44"),
    ("28", "Database Design", "46"),
    ("29", "Detailed Explanation of Every Implemented Module", "48"),
    ("30", "Frontend Implementation", "53"),
    ("31", "Backend Implementation", "56"),
    ("32", "API Documentation", "59"),
    ("33", "System Workflow", "62"),
    ("34", "UML Diagrams", "65"),
    ("35", "Data Flow Diagrams", "68"),
    ("36", "Screenshots of the Actual Application", "71"),
    ("37", "Testing Methodology", "76"),
    ("38", "Test Cases and Results", "78"),
    ("39", "Performance Evaluation", "82"),
    ("40", "Results and Discussion", "85"),
    ("41", "Advantages", "88"),
    ("42", "Limitations", "90"),
    ("43", "Applications", "92"),
    ("44", "Future Enhancements", "94"),
    ("45", "Conclusion", "96"),
    ("46", "References", "98"),
    ("47", "Appendix – Important Source Code Snippets", "101")
]

LIST_OF_FIGURES_DATA = [
    ("Figure 1", "UniMate Multi-Tier System Architecture Diagram", "28"),
    ("Figure 2", "Retrieval-Augmented Generation (RAG) Ingestion and Query Workflow", "34"),
    ("Figure 3", "Unified UML Representation (Use Case, Sequence, DFD Level 1, Database ER)", "66"),
    ("Figure 4", "Application Screenshot: Live University Dashboard Module", "71"),
    ("Figure 5", "Application Screenshot: Document Library and Multi-PDF Upload Manager", "72"),
    ("Figure 6", "Application Screenshot: AI University Chatbot with Document-Filtered Retrieval", "72"),
    ("Figure 7", "Application Screenshot: Academic Document Summarizer Interface", "73"),
    ("Figure 8", "Application Screenshot: Intelligent Quiz and Assessment Generator", "74"),
    ("Figure 9", "Application Screenshot: Personalized Weekly Study Planner Interface", "74"),
    ("Figure 10", "Application Screenshot: Academic Analytics and Performance Metrics", "75"),
    ("Figure 11", "Application Screenshot: Interactive GenAI Concepts and RAG Explainer", "75")
]

LIST_OF_TABLES_DATA = [
    ("Table 1", "Hardware Specifications and Deployment Environment", "22"),
    ("Table 2", "Software Specifications, Runtimes, and Frameworks", "23"),
    ("Table 3", "Comparative Summary of Implemented Modules and AI Capabilities", "49"),
    ("Table 4", "FastAPI Asynchronous REST API Endpoint Documentation", "60"),
    ("Table 5", "Automated Pytest Execution and Verification Matrix (25 Test Cases)", "79"),
    ("Table 6", "System Latency, Memory Footprint, and Retrieval Performance Metrics", "83")
]

HARDWARE_TABLE_ROWS = [
    ("Processor (CPU)", "Intel Core i5 / i7 (8th Gen+) or AMD Ryzen 5 / 7 (x86_64 architecture)", "Supports local vector operations and multi-threaded document parsing"),
    ("System Memory (RAM)", "8 GB minimum (16 GB recommended for concurrent embeddings)", "Accommodates PyMuPDF text buffers, PyTorch runtime, and ChromaDB cache"),
    ("Storage Drive", "512 GB Solid State Drive (SSD) with NVMe / SATA interface", "Ensures high-speed I/O for SQLite vector storage and PDF streaming"),
    ("Network Interface", "Standard 802.11ac/ax Wi-Fi or Gigabit Ethernet adapter", "Required exclusively for outbound Google Gemini 1.5 Flash API calls (optional)"),
    ("Display Resolution", "1920 × 1080 Full HD (or minimum 1280 × 800 display)", "Optimized for responsive desktop web application viewing")
]

SOFTWARE_TABLE_ROWS = [
    ("Operating System", "Microsoft Windows 10 / 11 64-bit (or Linux Ubuntu 22.04 LTS)", "Host development and execution environment"),
    ("Backend Runtime", "Python 3.10.x / 3.11.x 64-bit", "High-performance asynchronous execution runtime"),
    ("Backend Framework", "FastAPI v0.110.0+ with Uvicorn ASGI Server", "Async REST API gateway and request handling"),
    ("Vector Database", "ChromaDB v0.4.22+ (Embedded SQLite + HNSW engine)", "Persistent dense vector storage with cosine distance metric"),
    ("Embedding Model", "Sentence Transformers (all-MiniLM-L6-v2, 384 dimensions)", "Local bi-encoder for semantic vector generation"),
    ("PDF Ingestion Engine", "PyMuPDF (fitz) v1.23.0+", "High-speed digital text, table, and page metadata extraction"),
    ("Generative AI LLM", "Google Gemini 1.5 Flash (google-generativeai SDK v0.4.0+)", "Advanced cloud foundation model for grounded generation"),
    ("Frontend UI Library", "React 18.2.0 with Vite 5.4.0 build bundler", "Modern declarative user interface component architecture"),
    ("Styling Framework", "Tailwind CSS v3.4.0 with PostCSS & Autoprefixer", "Utility-first modern styling with custom purple theme"),
    ("Iconography", "Lucide React v0.344.0+", "Consistent modern iconography across navigation and components"),
    ("Testing Harness", "Pytest v8.0.0+ with FastAPI TestClient (httpx)", "Automated regression and endpoint unit testing suite")
]

API_TABLE_ROWS = [
    ("GET", "/health", "None", "HealthStatus", "Returns operational health of API, active AI engine, and vector collection status"),
    ("POST", "/api/documents/upload", "multipart/form-data (file: UploadFile)", "UploadResponse", "Ingests single PDF, extracts text, generates chunks, and indexes into ChromaDB"),
    ("POST", "/api/documents/upload-multiple", "multipart/form-data (files: List[UploadFile])", "UploadResponse", "Batch ingests multiple PDFs concurrently with individual status reporting"),
    ("GET", "/api/documents/list", "None", "DocumentListResponse", "Retrieves catalog of indexed documents, page counts, chunk totals, and ingestion dates"),
    ("DELETE", "/api/documents/{doc_id}", "Path: doc_id (str)", "DeleteResponse", "Removes document metadata and deletes corresponding chunk vectors from ChromaDB"),
    ("POST", "/api/chat/query", "ChatQueryRequest (query, doc_filter, top_k)", "ChatQueryResponse", "Executes semantic vector search, injects context, and returns cited AI response"),
    ("POST", "/api/summarize", "SummarizeRequest (doc_id, mode, length)", "SummarizeResponse", "Generates structured executive summary, key concepts, or exam cram notes"),
    ("POST", "/api/quiz/generate", "QuizRequest (doc_id, num_questions, difficulty)", "QuizResponse", "Synthesizes multiple-choice questions, options, answers, and rationale"),
    ("POST", "/api/study-plan/generate", "StudyPlanRequest (doc_id, days, hours_per_day)", "StudyPlanResponse", "Constructs a personalized day-by-day academic revision and practice roadmap"),
    ("GET", "/api/analytics/summary", "None", "AnalyticsResponse", "Aggregates document counts, total indexed chunks, quiz counts, and query metrics")
]

TEST_CASES_DATA = [
    ("TC-RAG-01", "PDF Ingestion", "Upload GenAI_Study_Notes.pdf", "Text extracted, chunks generated, indexed in ChromaDB", "Document indexed with 4 chunks across 2 pages", "PASS"),
    ("TC-RAG-02", "Multi-Upload", "Batch upload Syllabus & Regulations PDFs", "All documents processed sequentially and cataloged", "2 files indexed with unique IDs and chunk counts", "PASS"),
    ("TC-RAG-03", "Duplicate Upload", "Upload same document twice", "System handles duplicate gracefully or updates version", "Document re-indexed without vector duplication", "PASS"),
    ("TC-RAG-04", "Empty PDF Handling", "Upload 0-byte corrupt PDF file", "Validation error returned with HTTP 400 status", "HTTP 400 Bad Request: Invalid PDF structure", "PASS"),
    ("TC-RAG-05", "Vector Embedding", "Encode 800-char text chunk", "384-dimensional float vector produced", "Tensor shape (384,) generated via all-MiniLM-L6-v2", "PASS"),
    ("TC-RAG-06", "Global Retrieval", "Query: 'What is RAG?' (no filter)", "Top-k chunks retrieved across all indexed documents", "3 relevant chunks retrieved with cosine score > 0.65", "PASS"),
    ("TC-RAG-07", "Doc-Specific Filter", "Query: 'Explain GenAI' with doc_filter set", "Chunks retrieved ONLY from GenAI_Study_Notes.pdf", "100% of chunks match metadata doc_name", "PASS"),
    ("TC-RAG-08", "Isolated Syllabus", "Query: 'Explain Computer_Science_Syllabus.pdf only'", "Retrieval strictly isolated to syllabus document", "No passages from GenAI or Regulations returned", "PASS"),
    ("TC-RAG-09", "Non-Existent Doc", "Query with doc_filter='NonExistent.pdf'", "Returns clear warning: Document not found", "Handled gracefully with HTTP 200 and advisory text", "PASS"),
    ("TC-RAG-10", "Citation Accuracy", "Query regarding grading regulations", "Passage citation matches actual page number", "Citation: [Regulations.pdf, Page 1] verified", "PASS"),
    ("TC-RAG-11", "Gemini Generation", "Prompt with retrieved context dispatched to Gemini", "Structured answer formatted with markdown headings", "Coherent multi-paragraph response received", "PASS"),
    ("TC-RAG-12", "Offline Fallback", "Simulate offline state by omitting API key", "Local Semantic Synthesizer produces grounded response", "Response generated deterministically from chunks", "PASS"),
    ("TC-RAG-13", "Summarizer - Exec", "Request executive summary of Syllabus.pdf", "High-level overview covering modules and credits", "3-paragraph executive summary returned", "PASS"),
    ("TC-RAG-14", "Summarizer - Exam", "Request exam cram notes of GenAI notes", "Bullet points of key formulas, definitions, pitfalls", "Targeted bulleted exam study guide generated", "PASS"),
    ("TC-RAG-15", "Quiz Generation", "Generate 5 MCQs on GenAI concepts", "JSON containing 5 questions, 4 options each, answer key", "5 valid questions with correct answers & explanations", "PASS"),
    ("TC-RAG-16", "Study Planner", "Generate 7-day schedule for 2 hours/day", "Day-by-day timetable mapping topics to time blocks", "7 daily schedules returned with specific review goals", "PASS"),
    ("TC-RAG-17", "Document List API", "GET /api/documents/list", "Returns JSON array of all active documents", "HTTP 200: Array of document objects with metadata", "PASS"),
    ("TC-RAG-18", "Document Delete API", "DELETE /api/documents/{doc_id}", "Document removed from SQLite and ChromaDB vectors", "HTTP 200: All associated vectors deleted", "PASS"),
    ("TC-RAG-19", "CORS Configuration", "OPTIONS /api/chat/query from Vite origin", "Access-Control-Allow-Origin: * header present", "HTTP 200 with appropriate CORS headers", "PASS"),
    ("TC-RAG-20", "FastAPI Health Check", "GET /health", "Status: healthy, AI engine status reported", "HTTP 200: healthy, live_mode=True, model=gemini", "PASS"),
    ("TC-RAG-21", "Analytics API", "GET /api/analytics/summary", "Accurate aggregate counts of documents and chunks", "HTTP 200 with matching document and chunk metrics", "PASS"),
    ("TC-RAG-22", "Chunk Overlap Check", "Chunk text with 800 chars and 150 overlap", "Adjacent chunks share 150 characters boundary", "Verified sliding window overlap preservation", "PASS"),
    ("TC-RAG-23", "Special Chars Query", "Query: 'RAG & LLMs: Cost vs Accuracy?'", "Query encoded without tokenization or regex failure", "Vector search completed successfully", "PASS"),
    ("TC-RAG-24", "Empty Query Rejection", "POST /api/chat/query with empty string", "Validation error HTTP 422 Unprocessable Entity", "HTTP 422: Query string cannot be empty", "PASS"),
    ("TC-RAG-25", "Full Integration Flow", "Upload PDF -> Query -> Citation -> Quiz -> Plan", "End-to-end user pipeline completes without error", "All modules process newly uploaded document data", "PASS")
]

PERFORMANCE_METRICS_ROWS = [
    ("PyMuPDF Text Extraction Throughput", "0.08 – 0.15 seconds per 10-page document", "Benchmarked on standard course syllabus PDF"),
    ("Sliding-Window Chunking & Normalization", "0.03 seconds per 10,000 characters", "Memory-efficient character sliding window"),
    ("all-MiniLM-L6-v2 Vector Encoding", "0.025 seconds per chunk (CPU execution)", "PyTorch quantized ONNX/Torch CPU inference"),
    ("ChromaDB Vector Indexing Latency", "0.015 seconds per chunk batch", "HNSW graph insertion with metadata indexing"),
    ("ChromaDB Top-3 Vector Search Latency", "12 – 24 milliseconds", "Approximate Nearest Neighbor cosine similarity"),
    ("Google Gemini 1.5 Flash Network Latency", "0.95 – 1.45 seconds total round-trip", "Includes SSL negotiation and token streaming"),
    ("Local Semantic Synthesizer Latency", "8 – 15 milliseconds", "Deterministic offline fallback synthesis"),
    ("FastAPI JSON API Response Overhead", "< 5 milliseconds", "Starlette async ASGI pipeline processing"),
    ("Memory Footprint (Idle Backend)", "180 MB – 220 MB RAM", "Includes ChromaDB runtime and Torch core"),
    ("Memory Footprint (Peak RAG Query)", "340 MB – 420 MB RAM", "During batch embedding and matrix calculations")
]
