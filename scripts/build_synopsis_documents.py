import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

# -------------------------------------------------------------
# 1. CONTENT DATA DEFINITION (18 SECTIONS)
# -------------------------------------------------------------

SYNOPSIS_TITLE = "UniMate: An Intelligent University Assistant Using Generative Artificial Intelligence and Large Language Models (LLMs)"
STUDENT_NAME = "Pavan Prakash Naik"
STUDENT_USN = "SCA25MSD051"
DEPT_NAME = "[DEPARTMENT_OF_COMPUTER_SCIENCE_AND_ENGINEERING]"
COLLEGE_NAME = "[INSTITUTION_COLLEGE_NAME_PLACEHOLDER]"
UNIVERSITY_NAME = "[AFFILIATED_UNIVERSITY_NAME_PLACEHOLDER]"
GUIDE_NAME = "[FACULTY_GUIDE_NAME_PLACEHOLDER]"
GUIDE_DESIGNATION = "[DESIGNATION_PLACEHOLDER]"
ACADEMIC_YEAR = "2025 – 2026 / [ACADEMIC_YEAR_PLACEHOLDER]"

# Text content definitions for all sections
CONTENT = {
    "abstract": (
        "University students routinely navigate voluminous, fragmented academic documents including course syllabi, "
        "lecture notes, examination guidelines, and institutional academic regulations. Traditional campus web portals "
        "and learning management systems (LMS) rely on rigid keyword searches, requiring tedious manual document navigation. "
        "Conversely, raw commercial Large Language Models (LLMs) frequently suffer from factual hallucinations, lack access to "
        "private institutional courseware, and fail to provide verifiable source citations. "
        "To resolve these challenges, this project presents UniMate—an autonomous, full-stack, AI-powered university assistant "
        "built on a localized Retrieval-Augmented Generation (RAG) architecture. "
        "UniMate allows students to upload official university PDFs, extracts digital text page-by-page using PyMuPDF, divides content "
        "into overlapping semantic chunks, and generates 384-dimensional dense numerical embeddings using Sentence Transformers "
        "(all-MiniLM-L6-v2). Embeddings and granular metadata (document ID, filename, and page number) are persistently indexed "
        "in ChromaDB. Upon receiving a natural language question, the system performs cosine similarity vector search, retrieves the most "
        "semantically relevant passages, and constructs a grounded prompt for the Google Gemini 1.5 Flash foundation model. "
        "The model synthesizes coherent, comprehensive academic answers with exact page-level citations. Beyond Q&A, UniMate incorporates "
        "an AI Notes Summarizer (supporting seven academic summary modes), an interactive Multiple Choice Quiz Generator with detailed "
        "rationales, an automated Day-by-Day Study Planner with interactive completion tracking, an Analytics dashboard, and an educational "
        "GenAI Concepts module. Experimental verification confirms zero cross-document contamination, accurate citation tracing, "
        "and complete local execution without external cloud dependencies beyond the optional Gemini API."
    ),
    "introduction": (
        "The rapid evolution of Artificial Intelligence, specifically Generative AI and Large Language Models, has transformed "
        "human-computer interaction across professional and educational domains. In higher education institutions, academic "
        "information is primarily disseminated through unstructured portable document format (PDF) files. Students must synthesize "
        "extensive curricula, adhere to intricate evaluation rules, and organize intensive examination revision across multiple disparate "
        "documents. Conventional search mechanisms (such as Ctrl+F or portal search bars) fail to capture semantic context, conceptual "
        "analogies, or cross-document comparisons. While foundation models like Google Gemini and OpenAI GPT offer powerful linguistic "
        "reasoning, their generic pre-training data lacks institutional policies and proprietary course syllabi, often generating plausible "
        "yet factually incorrect statements (hallucinations).\n\n"
        "Retrieval-Augmented Generation (RAG) provides an optimal architectural solution by decoupling parametric linguistic intelligence "
        "from non-parametric factual storage. UniMate bridges the gap between academic documents and intelligent assistance by combining "
        "a modern React 18 single-page application with a high-performance Python FastAPI backend, ChromaDB vector indexing, and Google Gemini "
        "LLM synthesis. The system operates locally on consumer hardware, ensuring student privacy, zero infrastructure licensing cost, "
        "and immediate response latency."
    ),
    "problem_statement": (
        "Higher education students face critical cognitive friction when accessing, analyzing, and revising academic materials:\n\n"
        "1. Information Fragmentation & Search Inefficiency: Vital academic data (passing thresholds, attendance condonation rules, syllabus modules, "
        "exam schedules) is dispersed across numerous multi-page PDFs. Finding specific policies requires laborious manual reading.\n"
        "2. LLM Hallucinations in Educational Settings: When students query general-purpose AI chatbots regarding their specific college syllabus "
        "or examination scheme, the models invent non-existent course codes, fabricate grading formulas, and misquote regulations.\n"
        "3. Absence of Verifiable Citations: Standard AI chatbots do not furnish reliable citations, preventing students from cross-verifying "
        "answers against official university handbooks.\n"
        "4. Lack of Integrated Academic Tools: Students currently depend on disconnected software—separate tools for PDF viewing, flashcard "
        "generation, quiz creation, and study timetable scheduling—leading to disrupted learning workflows."
    ),
    "objectives": [
        ("Contextual RAG Retrieval", "Implement an end-to-end local RAG pipeline that accurately answers student academic queries using uploaded university documents without factual hallucinations."),
        ("Verifiable Source Citations", "Ensure 100% of generated responses provide transparent page-level citations (document name and exact page number) derived strictly from retrieved passages."),
        ("Multi-Document Management", "Build an in-memory validated PDF upload and indexing engine supporting multiple files, duplicate replacement, and metadata preservation in ChromaDB."),
        ("Examination Preparation Tools", "Develop an AI Summarizer offering 7 distinct academic summary formats and an automated Multiple Choice Quiz Generator with immediate score feedback and rationales."),
        ("Personalized Study Planning", "Create an automated revision planner that synthesizes day-by-day study timetables based on subject difficulty, target exam dates, and daily study hour allocations."),
        ("Professional Responsive Web Application", "Deliver a cohesive SaaS-style interface using React, Tailwind CSS, Lucide icons, and Recharts, deployable locally on standard student laptops.")
    ],
    "existing_system": (
        "The existing academic information environment in universities relies predominantly on manual retrieval and generic tools:\n\n"
        "• Traditional Campus Portals & Static Websites: Universities host documents on static departmental pages. Search utilities are limited "
        "to exact keyword matching on file titles rather than semantic document contents.\n"
        "• Manual Scanning (Ctrl+F): Students manually search PDFs using keyword queries, which fails when queries use synonyms, acronyms, or conceptual phrasing.\n"
        "• Standalone Public Chatbots (ChatGPT / Gemini Free Tier): Students paste questions into commercial web chatbots. These models answer from "
        "outdated pre-training corpora, cannot read local college circulars, and cannot provide verifiable page citations.\n"
        "• Disconnected Productivity Applications: Practice quizzes and revision schedules must be created manually or through disconnected "
        "third-party subscription platforms that lack syllabus awareness."
    ),
    "proposed_system": (
        "UniMate addresses the deficiencies of the existing ecosystem through a unified, localized, RAG-driven academic portal:\n\n"
        "• Semantic Vector Search: Replaces rigid keyword matching with 384-dimensional dense semantic embeddings using Sentence Transformers, "
        "enabling the system to understand synonyms, natural language queries, and conceptual relationships.\n"
        "• Grounded Context Augmentation: Chunks retrieved from authorized PDFs are injected directly into the LLM system prompt, constraining "
        "the model to answer solely from authoritative source material.\n"
        "• Strict Citation Tracing: Every chunk retains metadata tracking its original filename, document ID, and page number, enabling UniMate "
        "to append verified citation badges to every statement.\n"
        "• Dual AI Reasoning Engine: Integrates the Google Gemini 1.5 Flash API for low-latency live reasoning, paired with a deterministic Local Semantic "
        "Synthesizer that guarantees complete sentence generation and structured responses even in offline environments.\n"
        "• Integrated Academic Suite: Combines document Q&A, exam summarization, interactive self-assessment quizzes, and customizable daily "
        "study schedules within a single dashboard."
    ),
    "scope": (
        "The project scope encompasses undergraduate and postgraduate academic assistance across standard university document categories:\n\n"
        "• Covered Document Types: Course syllabi, departmental lecture notes, official academic regulations, student handbooks, and examination guidelines.\n"
        "• Operational Environment: Runs locally on standard consumer Windows 10/11 laptops without requiring specialized GPU infrastructure.\n"
        "• User Interaction: Multi-turn natural language conversational chat, targeted document-specific retrieval (e.g., 'Explain CS-401 Syllabus only'), "
        "interactive quizzes with performance history, and visual study schedule tracking.\n"
        "• Security & Privacy: Local vector indexing prevents unauthorized dissemination of proprietary lecture notes or draft university circulars."
    ),
    "hardware_reqs": [
        ("Processor (CPU)", "Intel Core i3 / AMD Ryzen 3 or higher (Quad-Core 2.0 GHz recommended)"),
        ("System Memory (RAM)", "8 GB RAM minimum (16 GB recommended for seamless local vectorization)"),
        ("Storage Capacity", "Minimum 10 GB available SSD / HDD space (for Python environment, ChromaDB, and document uploads)"),
        ("Display Resolution", "1366 x 768 minimum display resolution (1920 x 1080 Full HD recommended)"),
        ("Network Interface", "Standard Wi-Fi / Ethernet adapter (required only for Gemini API access; not required for local mode)")
    ],
    "software_reqs": [
        ("Operating System", "Microsoft Windows 10 / 11 (64-bit)"),
        ("Runtime Environment", "Python 3.10.x (64-bit) & Node.js LTS v20.x"),
        ("Backend Framework", "FastAPI v0.115+ with Uvicorn ASGI Web Server"),
        ("Frontend Technology", "React 18.3, Vite 5.4, Tailwind CSS 3.4, Lucide React, Recharts"),
        ("Vector Database", "ChromaDB v0.5+ (Persistent Local Client with HNSW indexing)"),
        ("Embedding Model", "Sentence Transformers (sentence-transformers/all-MiniLM-L6-v2)"),
        ("PDF Processing Engine", "PyMuPDF (fitz v1.24+)"),
        ("Relational Database", "SQLite 3 (Embedded SQL engine)"),
        ("Modern Web Browser", "Google Chrome, Mozilla Firefox, or Microsoft Edge (modern Chromium-based)")
    ],
    "technologies": [
        ("React 18 & Vite", "Provides a lightning-fast, reactive single-page user interface with modular component architecture and hot-module replacement during development."),
        ("Tailwind CSS", "Utility-first CSS framework enabling a sleek, SaaS-grade purple/indigo academic design system with responsive card layouts and smooth transitions."),
        ("Python & FastAPI", "High-performance, asynchronous REST API backend powering document ingestion, vector orchestration, database transactions, and model routing."),
        ("Google Gemini API", "Foundation model API (Gemini 1.5 Flash) delivering rapid cognitive synthesis, format compliance, and contextual reasoning over injected document context."),
        ("Sentence Transformers", "Pre-trained transformer model (`all-MiniLM-L6-v2`) generating dense 384-dimensional semantic embeddings for sentences and paragraphs."),
        ("ChromaDB", "Lightweight, open-source, embeddable vector database executing approximate nearest-neighbor (HNSW) search with cosine similarity and metadata filtering."),
        ("PyMuPDF (fitz)", "High-speed digital PDF parser extracting structured textual streams while accurately preserving sequential page numbers and metadata."),
        ("SQLite", "Embedded, zero-configuration relational database managing application state: document records, user conversations, chat messages, quizzes, and study plans.")
    ],
    "methodology_steps": [
        ("1. PDF Document Upload", "Students upload official university PDFs via a multipart/form-data interface. In-memory validation checks MIME type, file size (<=25MB), and PDF integrity before disk persistence."),
        ("2. Page-Preserving Text Extraction", "PyMuPDF parses the document stream page by page. Text is cleaned by stripping extraneous formatting and excessive whitespace while recording exact page numbers."),
        ("3. Sliding-Window Text Chunking", "Extracted text is split into semantic chunks (800 characters with 150-character overlap). The algorithm respects word and sentence boundaries to preserve coherent conceptual thoughts."),
        ("4. Dense Numerical Embedding", "Chunks are passed through the Sentence Transformer model (`all-MiniLM-L6-v2`), generating normalized 384-dimensional continuous vector representations."),
        ("5. Persistent ChromaDB Vector Indexing", "Vectors and associated metadata (`doc_id`, `doc_name`, `page_number`, `chunk_index`) are inserted into ChromaDB's persistent collection using an HNSW graph index."),
        ("6. Semantic Similarity Retrieval", "When a student submits a query, the text is converted into an embedding. ChromaDB executes cosine similarity search, applying metadata filters if a specific document was targeted."),
        ("7. Context-Aware Prompt Construction", "The top-k retrieved passages are assembled into a structured system prompt. System directives constrain the model to derive conclusions strictly from the excerpts."),
        ("8. Grounded LLM Synthesis & Citations", "Google Gemini (or the Local Synthesizer) generates a comprehensive Markdown response. Verified citation badges listing document name and page number are appended to the response.")
    ],
    "modules": [
        ("AI Academic Chatbot", "Conversational multi-turn assistant enabling natural language queries across all indexed materials or targeted single documents with exact page citations and chat history."),
        ("Document Management", "Upload, manage, inspect, and delete university PDFs. Features live indexing status badges, upload timestamp tracking, file size metrics, and duplicate safe replacement."),
        ("AI Notes Summarizer", "Synthesizes multi-format study notes from uploaded PDFs across 7 academic modes: Detailed, Executive Short, Key Points, Definitions, Exam Topics, Rapid Revision, and Simple Language."),
        ("AI Quiz Generator", "Generates 4-option multiple choice questions across Easy, Medium, and Difficult tiers. Features instant score calculation, detailed rationales for correct/incorrect answers, and attempt history."),
        ("AI Study Planner", "Creates customized day-by-day revision timetables based on subject difficulty, target exam dates, and daily study hours. Includes interactive SQLite topic completion checkboxes."),
        ("Academic Analytics", "Visualizes learning engagement using Recharts: total documents indexed, questions answered, average quiz scores, study completion percentages, and real-time audit trails."),
        ("GenAI Concepts Repository", "Interactive educational reference module explaining core GenAI foundations: Transformers, Multi-Head Self-Attention, RAG architectures, Embeddings, and Prompt Engineering.")
    ],
    "expected_outcomes": [
        "Elimination of Academic Hallucinations: Zero unverified statements; responses are strictly bound to official uploaded documents.",
        "Significant Time Savings: Reduces time spent manually scanning multi-hundred-page syllabi and handbooks from hours to seconds.",
        "Transparent Citation Verification: Empowers students to cross-check every AI assertion with exact page references.",
        "Structured Examination Readiness: Facilitates rapid self-assessment through dynamic quizzes and customized revision timetables.",
        "Data Privacy & Local Independence: Operates entirely on standard local hardware without exposing private academic files to third-party public repositories."
    ],
    "applications": [
        "University Students: Preparing for semester examinations, understanding prerequisite course modules, and clarifying grading regulations.",
        "Faculty & Academic Advisors: Rapidly verifying departmental course requirements and addressing student queries regarding attendance and condonation policies.",
        "Departmental Examination Cells: Automating helpdesk responses for hall ticket policies, exam timing rules, and malpractice procedures.",
        "Distance Education & E-Learning Platforms: Providing 24/7 automated academic advisory services for remote students without physical office access."
    ],
    "future_enhancements": [
        "Multilingual Regional Translation: Extending the RAG pipeline to synthesize lecture notes and summaries in regional languages.",
        "Handwritten Whiteboard OCR: Integrating optical character recognition (OCR) models to ingest handwritten lecture notes and classroom whiteboard photos.",
        "Voice-Activated Conversational Interface: Implementing speech-to-text (Whisper) and text-to-speech models to support visually impaired students.",
        "Direct LMS Integration: Connecting directly to Canvas, Moodle, and Google Classroom APIs for automatic syllabus synchronization."
    ],
    "conclusion": (
        "UniMate demonstrates the practical, ethical, and high-impact application of Generative Artificial Intelligence and Large Language Models "
        "to university education. By implementing a robust, localized Retrieval-Augmented Generation pipeline, the system effectively overcomes "
        "the primary limitation of commercial foundation models: factual hallucination. By pairing PyMuPDF text extraction, Sentence Transformers dense "
        "embeddings, ChromaDB vector indexing, and Google Gemini reasoning, UniMate provides university students with reliable, document-grounded "
        "answers accompanied by verifiable page-level citations. The inclusion of academic summarization, dynamic quiz generation, and personalized "
        "study planning establishes UniMate as a comprehensive, production-ready educational assistant. The project successfully validates that "
        "advanced GenAI architectures can be deployed locally on consumer-grade student laptops, ensuring accessibility, data privacy, and academic integrity."
    ),
    "references": [
        "Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30, 5998–6008.",
        "Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing Systems, 33, 9459–9474.",
        "Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP), 3982–3992.",
        "Team, G., Anil, R., Borgeaud, S., Wu, Y., Alayrac, J. B., Yu, J., Soricut, R., Schalkwyk, J., Dai, A. M., Hauth, A., et al. (2023). Gemini: A family of highly capable multimodal models. arXiv preprint arXiv:2312.11805.",
        "ChromaDB Authors. (2024). Chroma: The open-source embedding database. https://www.trychroma.com/docs.",
        "Tiangolo, S. (2024). FastAPI: High performance, easy to learn, fast to code, ready for production. https://fastapi.tiangolo.com/.",
        "McKie, P., & Liu, J. (2024). PyMuPDF: Python bindings for MuPDF rendering library. https://pymupdf.readthedocs.io/."
    ]
}

# -------------------------------------------------------------
# 2. DOCX GENERATION FUNCTION
# -------------------------------------------------------------

def build_docx_synopsis(output_path="UniMate_Project_Synopsis.docx", diagram_path="architecture_diagram.png"):
    doc = docx.Document()

    # Set Margins and Headers/Footers
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.header_distance = Inches(0.5)
        section.footer_distance = Inches(0.5)
        section.different_first_page_header_footer = True

        # Header for body pages
        hdr = section.header
        hdr_p = hdr.paragraphs[0]
        hdr_p.text = "UniMate: Project Synopsis | Generative AI & Large Language Models"
        hdr_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if hdr_p.runs:
            hdr_p.runs[0].font.name = 'Times New Roman'
            hdr_p.runs[0].font.size = Pt(8.5)
            hdr_p.runs[0].font.color.rgb = RGBColor(100, 116, 139)

        # Footer for body pages
        ftr = section.footer
        ftr_p = ftr.paragraphs[0]
        ftr_p.text = f"Candidate: {STUDENT_NAME} (USN: {STUDENT_USN})"
        ftr_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if ftr_p.runs:
            ftr_p.runs[0].font.name = 'Times New Roman'
            ftr_p.runs[0].font.size = Pt(8.5)
            ftr_p.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    # Styles setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(30, 41, 59) # Slate 800

    # Helper function for adding headings
    def add_sec_heading(title, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.name = 'Times New Roman'
        run.bold = True
        if level == 1:
            run.font.size = Pt(13)
            run.font.color.rgb = RGBColor(30, 27, 75) # Navy
        else:
            run.font.size = Pt(11.5)
            run.font.color.rgb = RGBColor(51, 65, 85) # Slate 700
        return p

    def add_body_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        return p

    # --- COVER PAGE ---
    cover_title_p = doc.add_paragraph()
    cover_title_p.paragraph_format.space_before = Pt(36)
    cover_title_p.paragraph_format.space_after = Pt(12)
    cover_title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = cover_title_p.add_run(SYNOPSIS_TITLE)
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(17)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(30, 27, 75)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(28)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("A PROJECT SYNOPSIS\nSUBMITTED IN PARTIAL FULFILLMENT OF THE ACADEMIC CURRICULUM")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    # Submission table on cover page
    tbl = doc.add_table(rows=5, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_data = [
        ("Candidate Name:", f"{STUDENT_NAME}"),
        ("University Seat Number (USN):", f"{STUDENT_USN}"),
        ("Faculty Guide:", f"{GUIDE_NAME}, {GUIDE_DESIGNATION}"),
        ("Department & Institution:", f"{DEPT_NAME}\n{COLLEGE_NAME}\nAffiliated to {UNIVERSITY_NAME}"),
        ("Academic Year:", f"{ACADEMIC_YEAR}")
    ]
    for row_idx, (label, val) in enumerate(tbl_data):
        row = tbl.rows[row_idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.5)
        cell_val.width = Inches(3.8)
        
        p0 = cell_lbl.paragraphs[0]
        p0.paragraph_format.space_after = Pt(4)
        r0 = p0.add_run(label)
        r0.font.name = 'Times New Roman'
        r0.bold = True
        r0.font.size = Pt(10.5)

        p1 = cell_val.paragraphs[0]
        p1.paragraph_format.space_after = Pt(4)
        r1 = p1.add_run(val)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)

    doc.add_page_break()

    # --- SECTION 2: ABSTRACT ---
    add_sec_heading("2. Abstract")
    add_body_p(CONTENT["abstract"])

    # --- SECTION 3: INTRODUCTION ---
    add_sec_heading("3. Introduction")
    for para in CONTENT["introduction"].split("\n\n"):
        add_body_p(para)

    # --- SECTION 4: PROBLEM STATEMENT ---
    add_sec_heading("4. Problem Statement")
    for para in CONTENT["problem_statement"].split("\n\n"):
        add_body_p(para)

    # --- SECTION 5: OBJECTIVES OF THE PROJECT ---
    add_sec_heading("5. Objectives of the Project")
    for title, desc in CONTENT["objectives"]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_b = p.add_run(f"{title}: ")
        r_b.bold = True
        r_b.font.name = 'Times New Roman'
        r_d = p.add_run(desc)
        r_d.font.name = 'Times New Roman'

    # --- SECTION 6: EXISTING SYSTEM ---
    add_sec_heading("6. Existing System")
    for para in CONTENT["existing_system"].split("\n\n"):
        add_body_p(para)

    # --- SECTION 7: PROPOSED SYSTEM ---
    add_sec_heading("7. Proposed System")
    for para in CONTENT["proposed_system"].split("\n\n"):
        add_body_p(para)

    # --- SECTION 8: SCOPE OF THE PROJECT ---
    add_sec_heading("8. Scope of the Project")
    for para in CONTENT["scope"].split("\n\n"):
        add_body_p(para)

    # --- SECTION 9: SYSTEM REQUIREMENTS ---
    add_sec_heading("9. System Requirements")
    add_sec_heading("9.1 Hardware Requirements", level=2)
    t_hw = doc.add_table(rows=1 + len(CONTENT["hardware_reqs"]), cols=2)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hw.rows[0].cells[0].paragraphs[0].add_run("Hardware Component").bold = True
    t_hw.rows[0].cells[1].paragraphs[0].add_run("Minimum / Recommended Specification").bold = True
    for i, (comp, spec) in enumerate(CONTENT["hardware_reqs"]):
        t_hw.rows[i+1].cells[0].paragraphs[0].add_run(comp)
        t_hw.rows[i+1].cells[1].paragraphs[0].add_run(spec)

    add_sec_heading("9.2 Software Requirements", level=2)
    t_sw = doc.add_table(rows=1 + len(CONTENT["software_reqs"]), cols=2)
    t_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sw.rows[0].cells[0].paragraphs[0].add_run("Software Component").bold = True
    t_sw.rows[0].cells[1].paragraphs[0].add_run("Specification / Tool Used").bold = True
    for i, (comp, spec) in enumerate(CONTENT["software_reqs"]):
        t_sw.rows[i+1].cells[0].paragraphs[0].add_run(comp)
        t_sw.rows[i+1].cells[1].paragraphs[0].add_run(spec)

    # --- SECTION 10: SYSTEM ARCHITECTURE ---
    add_sec_heading("10. System Architecture")
    add_body_p(
        "UniMate is organized into a modular multi-tier architecture encompassing the Client Presentation Tier (React 18), "
        "API Gateway & Controller Tier (FastAPI), Document Processing Engine (PyMuPDF), Vector Embeddings & Storage Tier "
        "(Sentence Transformers & ChromaDB), and Cognitive Reasoning Tier (Google Gemini 1.5 Flash and Local Semantic Synthesizer). "
        "Figure 1 illustrates the end-to-end data flow from user interaction to grounded citation synthesis."
    )
    if os.path.exists(diagram_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(diagram_path, width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run("Figure 1: UniMate Multi-Tier System Architecture and Retrieval-Augmented Generation Pipeline.")
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(9.5)
        r_cap.italic = True

    # --- SECTION 11: TECHNOLOGIES USED ---
    add_sec_heading("11. Technologies Used")
    t_tech = doc.add_table(rows=1 + len(CONTENT["technologies"]), cols=2)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tech.rows[0].cells[0].paragraphs[0].add_run("Technology / Library").bold = True
    t_tech.rows[0].cells[1].paragraphs[0].add_run("Role in UniMate").bold = True
    for i, (tech, role) in enumerate(CONTENT["technologies"]):
        t_tech.rows[i+1].cells[0].paragraphs[0].add_run(tech).bold = True
        t_tech.rows[i+1].cells[1].paragraphs[0].add_run(role)

    # --- SECTION 12: METHODOLOGY ---
    add_sec_heading("12. Methodology")
    add_body_p(
        "The project methodology follows an iterative RAG engineering pipeline designed to guarantee verifiable citations and sub-second retrieval latency:"
    )
    for title, desc in CONTENT["methodology_steps"]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_b = p.add_run(f"{title}: ")
        r_b.bold = True
        r_b.font.name = 'Times New Roman'
        r_d = p.add_run(desc)
        r_d.font.name = 'Times New Roman'

    # --- SECTION 13: MAIN MODULES ---
    add_sec_heading("13. Main Modules of UniMate")
    for title, desc in CONTENT["modules"]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_b = p.add_run(f"{title}: ")
        r_b.bold = True
        r_b.font.name = 'Times New Roman'
        r_d = p.add_run(desc)
        r_d.font.name = 'Times New Roman'

    # --- SECTION 14: EXPECTED OUTCOMES ---
    add_sec_heading("14. Expected Outcomes")
    for out in CONTENT["expected_outcomes"]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(out)
        r.font.name = 'Times New Roman'

    # --- SECTION 15: APPLICATIONS ---
    add_sec_heading("15. Applications of UniMate")
    for app_item in CONTENT["applications"]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(app_item)
        r.font.name = 'Times New Roman'

    # --- SECTION 16: FUTURE ENHANCEMENTS ---
    add_sec_heading("16. Future Enhancements")
    for enh in CONTENT["future_enhancements"]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(enh)
        r.font.name = 'Times New Roman'

    # --- SECTION 17: CONCLUSION ---
    add_sec_heading("17. Conclusion")
    add_body_p(CONTENT["conclusion"])

    # --- SECTION 18: REFERENCES ---
    add_sec_heading("18. References")
    for idx, ref in enumerate(CONTENT["references"]):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(f"[{idx+1}] {ref}")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)

    doc.save(output_path)
    print(f"DOCX synopsis saved successfully at {output_path}")


# -------------------------------------------------------------
# 3. REPORTLAB NUMBERED CANVAS (PAGE X OF Y)
# -------------------------------------------------------------

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        # Do not draw headers/footers on cover page (page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Times-Roman", 8.5)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header
        self.setLineWidth(0.5)
        self.line(54, 750, 558, 750)
        self.drawString(54, 755, "UniMate: An Intelligent University Assistant Using GenAI & LLMs — Project Synopsis")

        # Running Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 33, f"Candidate: {STUDENT_NAME} (USN: {STUDENT_USN})")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 33, page_str)

        self.restoreState()


# -------------------------------------------------------------
# 4. PDF GENERATION FUNCTION
# -------------------------------------------------------------

def build_pdf_synopsis(output_path="UniMate_Project_Synopsis.pdf", diagram_path="architecture_diagram.png"):
    pdf_doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Academic Typography Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1e1b4b'),
        spaceAfter=14
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#475569'),
        spaceAfter=24
    )

    style_h1 = ParagraphStyle(
        'SynopsisH1',
        fontName='Times-Bold',
        fontSize=12.5,
        leading=15,
        textColor=colors.HexColor('#1e1b4b'),
        spaceBefore=11,
        spaceAfter=4,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'SynopsisH2',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'SynopsisBody',
        fontName='Times-Roman',
        fontSize=10,
        leading=13.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4
    )

    style_bullet = ParagraphStyle(
        'SynopsisBullet',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    style_table_hdr = ParagraphStyle(
        'TableHdr',
        fontName='Times-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#0f172a')
    )

    style_table_body = ParagraphStyle(
        'TableBody',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#334155')
    )

    style_caption = ParagraphStyle(
        'Caption',
        fontName='Times-Italic',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#475569'),
        spaceBefore=3,
        spaceAfter=6
    )

    story = []

    # ================= COVER PAGE =================
    story.append(Spacer(1, 35))
    story.append(Paragraph(SYNOPSIS_TITLE, style_cover_title))
    story.append(Paragraph("A PROJECT SYNOPSIS SUBMITTED IN PARTIAL FULFILLMENT OF THE<br/>REQUIREMENTS FOR THE DEGREE OF BACHELOR / MASTER OF TECHNOLOGY", style_cover_sub))
    story.append(HRFlowable(width="90%", thickness=1.5, color=colors.HexColor('#1e1b4b'), spaceBefore=5, spaceAfter=25))

    # Cover table
    cover_data = [
        [Paragraph("<b>Submitted By:</b>", style_table_hdr), Paragraph(f"<b>{STUDENT_NAME}</b><br/>USN: <b>{STUDENT_USN}</b>", style_table_body)],
        [Paragraph("<b>Under Guidance Of:</b>", style_table_hdr), Paragraph(f"<b>{GUIDE_NAME}</b><br/>{GUIDE_DESIGNATION}", style_table_body)],
        [Paragraph("<b>Department:</b>", style_table_hdr), Paragraph(f"{DEPT_NAME}", style_table_body)],
        [Paragraph("<b>Institution:</b>", style_table_hdr), Paragraph(f"{COLLEGE_NAME}<br/>Affiliated to {UNIVERSITY_NAME}", style_table_body)],
        [Paragraph("<b>Academic Year:</b>", style_table_hdr), Paragraph(f"{ACADEMIC_YEAR}", style_table_body)],
    ]
    t_cover = Table(cover_data, colWidths=[150, 320])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 40))
    story.append(Paragraph("[Confidential Document Prepared for Academic Evaluation]", ParagraphStyle('Conf', fontName='Times-Italic', fontSize=9, alignment=TA_CENTER, textColor=colors.HexColor('#64748b'))))
    story.append(PageBreak())

    # ================= 2. ABSTRACT =================
    story.append(Paragraph("2. Abstract", style_h1))
    story.append(Paragraph(CONTENT["abstract"], style_body))

    # ================= 3. INTRODUCTION =================
    story.append(Paragraph("3. Introduction", style_h1))
    for p_text in CONTENT["introduction"].split("\n\n"):
        story.append(Paragraph(p_text, style_body))

    # ================= 4. PROBLEM STATEMENT =================
    story.append(Paragraph("4. Problem Statement", style_h1))
    for p_text in CONTENT["problem_statement"].split("\n\n"):
        story.append(Paragraph(p_text, style_body))

    # ================= 5. OBJECTIVES =================
    story.append(Paragraph("5. Objectives of the Project", style_h1))
    for title, desc in CONTENT["objectives"]:
        bullet_text = f"• <b>{title}:</b> {desc}"
        story.append(Paragraph(bullet_text, style_bullet))

    # ================= 6. EXISTING SYSTEM =================
    story.append(Paragraph("6. Existing System", style_h1))
    for p_text in CONTENT["existing_system"].split("\n\n"):
        story.append(Paragraph(p_text, style_body))

    # ================= 7. PROPOSED SYSTEM =================
    story.append(Paragraph("7. Proposed System", style_h1))
    for p_text in CONTENT["proposed_system"].split("\n\n"):
        story.append(Paragraph(p_text, style_body))

    # ================= 8. SCOPE =================
    story.append(Paragraph("8. Scope of the Project", style_h1))
    for p_text in CONTENT["scope"].split("\n\n"):
        story.append(Paragraph(p_text, style_body))

    # ================= 9. SYSTEM REQUIREMENTS =================
    story.append(Paragraph("9. System Requirements", style_h1))
    story.append(Paragraph("9.1 Hardware Requirements", style_h2))
    
    hw_rows = [[Paragraph("<b>Component</b>", style_table_hdr), Paragraph("<b>Minimum Specification</b>", style_table_hdr)]]
    for comp, spec in CONTENT["hardware_reqs"]:
        hw_rows.append([Paragraph(comp, style_table_body), Paragraph(spec, style_table_body)])
    
    t_hw_pdf = Table(hw_rows, colWidths=[150, 350])
    t_hw_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_hw_pdf)

    story.append(Paragraph("9.2 Software Requirements", style_h2))
    sw_rows = [[Paragraph("<b>Component</b>", style_table_hdr), Paragraph("<b>Specification / Tool</b>", style_table_hdr)]]
    for comp, spec in CONTENT["software_reqs"]:
        sw_rows.append([Paragraph(comp, style_table_body), Paragraph(spec, style_table_body)])

    t_sw_pdf = Table(sw_rows, colWidths=[150, 350])
    t_sw_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sw_pdf)

    # ================= 10. SYSTEM ARCHITECTURE =================
    story.append(Paragraph("10. System Architecture", style_h1))
    story.append(Paragraph(
        "UniMate is structured into an interconnected five-tier system architecture: Client Presentation Tier (React 18), "
        "API Gateway & Controller Tier (FastAPI), Document Processing Engine (PyMuPDF), Vector Embeddings & Storage Tier "
        "(Sentence Transformers & ChromaDB), and Cognitive Reasoning Tier (Google Gemini 1.5 Flash and Local Semantic Synthesizer). "
        "Figure 1 illustrates the end-to-end data flow from user interaction to grounded citation synthesis.", style_body
    ))
    if os.path.exists(diagram_path):
        story.append(Spacer(1, 4))
        # 6.5 inches wide, 3.7 inches high fits neatly on letter page
        story.append(Image(diagram_path, width=6.5*inch, height=3.71*inch))
        story.append(Paragraph("Figure 1: UniMate Multi-Tier System Architecture and Retrieval-Augmented Generation Pipeline.", style_caption))

    # ================= 11. TECHNOLOGIES USED =================
    story.append(Paragraph("11. Technologies Used", style_h1))
    tech_rows = [[Paragraph("<b>Technology</b>", style_table_hdr), Paragraph("<b>Role & Technical Contribution</b>", style_table_hdr)]]
    for tech, role in CONTENT["technologies"]:
        tech_rows.append([Paragraph(f"<b>{tech}</b>", style_table_body), Paragraph(role, style_table_body)])

    t_tech_pdf = Table(tech_rows, colWidths=[130, 370])
    t_tech_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_tech_pdf)

    # ================= 12. METHODOLOGY =================
    story.append(Paragraph("12. Methodology", style_h1))
    story.append(Paragraph("The UniMate engineering methodology follows an eight-stage technical workflow:", style_body))
    for title, desc in CONTENT["methodology_steps"]:
        bullet_text = f"• <b>{title}:</b> {desc}"
        story.append(Paragraph(bullet_text, style_bullet))

    # ================= 13. MAIN MODULES =================
    story.append(Paragraph("13. Main Modules of UniMate", style_h1))
    for title, desc in CONTENT["modules"]:
        bullet_text = f"• <b>{title}:</b> {desc}"
        story.append(Paragraph(bullet_text, style_bullet))

    # ================= 14. EXPECTED OUTCOMES =================
    story.append(Paragraph("14. Expected Outcomes", style_h1))
    for out in CONTENT["expected_outcomes"]:
        story.append(Paragraph(f"• {out}", style_bullet))

    # ================= 15. APPLICATIONS =================
    story.append(Paragraph("15. Applications of UniMate", style_h1))
    for app_item in CONTENT["applications"]:
        story.append(Paragraph(f"• {app_item}", style_bullet))

    # ================= 16. FUTURE ENHANCEMENTS =================
    story.append(Paragraph("16. Future Enhancements", style_h1))
    for enh in CONTENT["future_enhancements"]:
        story.append(Paragraph(f"• {enh}", style_bullet))

    # ================= 17. CONCLUSION =================
    story.append(Paragraph("17. Conclusion", style_h1))
    story.append(Paragraph(CONTENT["conclusion"], style_body))

    # ================= 18. REFERENCES =================
    story.append(Paragraph("18. References", style_h1))
    for idx, ref in enumerate(CONTENT["references"]):
        ref_text = f"[{idx+1}] {ref}"
        story.append(Paragraph(ref_text, ParagraphStyle(
            f'Ref_{idx}',
            fontName='Times-Roman',
            fontSize=9,
            leading=12,
            leftIndent=18,
            firstLineIndent=-18,
            spaceAfter=3,
            textColor=colors.HexColor('#334155')
        )))

    pdf_doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF synopsis saved successfully at {output_path}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    docx_file = base_dir / "UniMate_Project_Synopsis.docx"
    pdf_file = base_dir / "UniMate_Project_Synopsis.pdf"
    diag_file = base_dir / "architecture_diagram.png"

    print("Building DOCX Synopsis...")
    build_docx_synopsis(str(docx_file), str(diag_file))

    print("Building PDF Synopsis...")
    build_pdf_synopsis(str(pdf_file), str(diag_file))

    print("Checking generated file sizes:")
    if docx_file.exists():
        print(f"DOCX: {docx_file.name} ({docx_file.stat().st_size / 1024:.1f} KB)")
    if pdf_file.exists():
        print(f"PDF:  {pdf_file.name} ({pdf_file.stat().st_size / (1024*1024):.2f} MB)")
