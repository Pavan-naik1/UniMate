import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors
from backend.app.core.config import settings
from backend.app.services.pdf_service import PDFService
from backend.app.rag.vector_store import vector_store
from backend.app.database import crud

SAMPLE_PDF_CONFIGS = [
    {
        "filename": "GenAI_Study_Notes.pdf",
        "title": "Demonstration: Generative AI and Large Language Models Comprehensive Notes",
        "author": "Department of Computer Science & AI",
        "sections": [
            ("1. Introduction to Generative Artificial Intelligence", 
             "Generative Artificial Intelligence (GenAI) refers to deep learning architectures capable of generating realistic, novel content such as text, images, code, and audio based on input prompts. Unlike discriminative models that predict a label y given input x (P(y|x)), generative models learn the joint probability distribution P(x, y) or data distribution P(x). The breakthrough in GenAI came with the Transformer architecture introduced by Vaswani et al. in 2017 ('Attention Is All You Need'), which replaced recurrent architectures with self-attention mechanisms allowing parallelized processing of textual tokens."),
            ("2. Large Language Model Architecture and Self-Attention",
             "Large Language Models (LLMs) are deep neural networks trained on vast textual corpora using auto-regressive next-token prediction objectives. The self-attention mechanism enables the model to weigh the contextual importance of every token relative to all other tokens in a sequence, regardless of their distance. Multi-head attention projects token representations into multiple distinct representation subspaces, enabling the capture of complex syntactic structures, long-range dependencies, and semantic relationships simultaneously. Parameters in modern LLMs range from hundreds of millions to hundreds of billions."),
            ("3. Retrieval-Augmented Generation (RAG) Architecture",
             "While LLMs possess impressive generalized reasoning capabilities, they suffer from knowledge cut-off limits, domain-specific ignorance, and hallucination (generating factually incorrect but fluent assertions). Retrieval-Augmented Generation (RAG) solves these limitations by coupling a non-parametric memory system (external vector database) with a parametric cognitive model (the LLM). When a query arrives, the system retrieves semantically relevant document chunks and prepends them as context into the prompt. This ensures verifiable grounding, eliminates the need for expensive continual fine-tuning, and provides direct page-level citations for university students."),
            ("4. Text Embeddings and Vector Databases",
             "Text embeddings are dense mathematical vectors in high-dimensional continuous vector space (e.g., 384 dimensions for all-MiniLM-L6-v2) that represent semantic concepts. Distances between vectors (measured via Cosine Similarity, Dot Product, or Euclidean distance) directly correspond to semantic similarities between textual passages. Vector databases like ChromaDB organize and index these high-dimensional embeddings using Approximate Nearest Neighbor (ANN) graphs such as Hierarchical Navigable Small World (HNSW), enabling millisecond retrieval across thousands of university document chunks.")
        ]
    },
    {
        "filename": "Computer_Science_Syllabus.pdf",
        "title": "Demonstration: University Course Syllabus – CS-401 GenAI & Intelligent Systems",
        "author": "Academic Curriculum Board",
        "sections": [
            ("Course Overview and Prerequisites",
             "Course Code: CS-401. Course Title: Generative AI and Intelligent Systems. Credits: 4 (Lecture: 3 hrs/week, Lab: 2 hrs/week). Prerequisites: Data Structures & Algorithms (CS-201), Linear Algebra & Probability (MA-202), and Object-Oriented Programming with Python (CS-204). This course provides theoretical foundations and hands-on software development principles for modern Generative AI, Large Language Models, and university-level societal applications."),
            ("Module 1: Foundations of Deep Learning and NLP",
             "Neural network architectures, word representations, Word2Vec, GloVe, Recurrent Neural Networks (RNN), Long Short-Term Memory (LSTM) networks, Gated Recurrent Units (GRU), Sequence-to-Sequence models, Encoder-Decoder paradigms, and early attention mechanisms."),
            ("Module 2: Transformer Architectures and Modern LLMs",
             "Self-attention formulation, Scaled Dot-Product Attention, Multi-Head Attention, Positional Encodings, Transformer Encoder and Decoder stacks. Pre-training objectives: Masked Language Modeling (BERT), Auto-regressive Generation (GPT), and Sequence-to-Sequence (T5). Multimodal models including Google Gemini."),
            ("Module 3: Retrieval-Augmented Generation and Vector Stores",
             "Limitations of standalone LLMs: hallucinations, latency, and knowledge obsolescence. RAG workflow: PDF text extraction using PyMuPDF, recursive character chunking with sliding window overlap, Sentence Transformers, vector indexing in ChromaDB, cosine similarity retrieval, prompt injection, and hallucination reduction."),
            ("Module 4: Examination Scheme and Capstone Evaluation",
             "Continuous Internal Evaluation (CIE): 50 Marks (2 Mid-term tests: 25 Marks, Assignment: 15 Marks, Quiz: 10 Marks). Semester End Examination (SEE): 50 Marks (Written Theory Exam: 3 hrs). University Capstone Project: Practical assessment evaluated on architecture design, working full-stack implementation, RAG pipeline integration, and formal academic documentation.")
        ]
    },
    {
        "filename": "University_Academic_Regulations.pdf",
        "title": "Demonstration: University Academic Regulations and Student Handbook",
        "author": "Office of Academic Affairs & Registrar",
        "sections": [
            ("Section 1: Minimum Attendance Requirements",
             "Every registered university student must maintain a minimum overall attendance of 75% in each registered theory and laboratory subject during the semester to become eligible to appear for the Semester End Examination (SEE). Attendance is calculated from the official commencement of classes to the final instructional day. Students falling below 75% will be marked as Not Eligible (NE) for that course."),
            ("Section 2: Attendance Condonation on Medical Grounds",
             "Under exceptional medical emergencies or sanctioned university sports representation, the Dean of Academic Affairs may condone attendance shortages of up to 10% (permitting students with between 65% and 74.9% attendance to write the examinations) upon submission of a genuine medical certificate verified by the University Medical Officer within seven days of recovery, accompanied by payment of the prescribed condonation fee."),
            ("Section 3: Grading System and Credit Calculation",
             "The university follows a 10-point Letter Grading Scale: Outstanding (O): 10 grade points (>=90 marks); Excellent (A+): 9 grade points (80-89 marks); Very Good (A): 8 grade points (70-79 marks); Good (B+): 7 grade points (60-69 marks); Above Average (B): 6 grade points (55-59 marks); Average (C): 5 grade points (50-54 marks); Fail (F): 0 grade points (<50 marks). Semester Grade Point Average (SGPA) is calculated as the sum of (Course Credits * Grade Points) divided by Total Semester Credits."),
            ("Section 4: Re-evaluation and Paper Verification Policy",
             "Students unsatisfied with their Semester End Examination marks may apply for Photocopy of Evaluated Answer Scripts and Re-evaluation within fifteen calendar days following the declaration of results. If the re-evaluation results in a mark difference exceeding 15% of the maximum marks, the paper is forwarded to an independent third evaluator, whose score shall be final.")
        ]
    },
    {
        "filename": "Examination_Guidelines.pdf",
        "title": "Demonstration: Examination Guidelines and Code of Conduct",
        "author": "Controller of Examinations",
        "sections": [
            ("1. Examination Timings and Reporting Protocol",
             "Morning examination sessions commence promptly at 09:30 AM and conclude at 12:30 PM. Afternoon sessions commence at 02:00 PM and conclude at 05:00 PM. Candidates must report to their assigned examination halls at least 20 minutes before the scheduled commencement. No student will be admitted into the examination hall after 15 minutes from the official start time."),
            ("2. Mandatory Hall Ticket and Student Identification",
             "Possession of the official printed University Examination Hall Ticket and valid University Identity Card is mandatory for entry. In case of lost hall tickets, students must obtain a provisional duplicate pass from the Controller of Examinations office at least two hours prior to the examination with a passport-size photograph."),
            ("3. Permitted and Prohibited Materials",
             "Permitted items include blue or black ink pens, non-programmable scientific calculators (models fx-82MS, fx-991MS or equivalent where specifically sanctioned on question paper), pencils, erasers, and transparent water bottles. Prohibited items include mobile phones, smartwatches, fitness bands, programmable calculators, loose sheets of paper, books, and digital storage media. Possession of unauthorized electronics inside the examination hall leads to immediate confiscation."),
            ("4. Malpractice Policy and Disciplinary Actions",
             "Any candidate found in possession of unauthorized materials, communicating with fellow candidates, copying, or attempting to impersonate another candidate will be booked under the University Malpractice Discipline Committee. Penalties range from cancellation of the specific paper to debarment from the university for up to three academic semesters depending on the severity of the offense.")
        ]
    }
]

def generate_sample_pdf(config: dict, output_dir: Path) -> Path:
    output_path = output_dir / config["filename"]
    if output_path.exists():
        return output_path
        
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom academic styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1e1b4b'),
        spaceAfter=10
    )
    
    author_style = ParagraphStyle(
        'DocAuthor',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4b5563'),
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#4338ca'),
        spaceBefore=14,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=8
    )
    
    disclaimer_style = ParagraphStyle(
        'DocDisclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#b91c1c'),
        spaceAfter=15
    )
    
    story = []
    story.append(Paragraph(config["title"], title_style))
    story.append(Paragraph(f"Published by: {config['author']} | University Academic Reference Document", author_style))
    story.append(Paragraph("[NOTE: This is an academic reference document developed for the UniMate AI Assistant Project.]", disclaimer_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=5, spaceAfter=15))
    
    for heading, text in config["sections"]:
        story.append(Paragraph(heading, h2_style))
        story.append(Paragraph(text, body_style))
        story.append(Spacer(1, 10))
        
    doc.build(story)
    return output_path

def seed_sample_documents_if_needed():
    """
    Ensures sample PDFs are created, and if no documents exist in SQLite,
    extracts, chunks, and indexes them in ChromaDB and SQLite.
    """
    settings.SAMPLE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    existing_docs = crud.get_documents()
    existing_names = {d["original_name"] for d in existing_docs}
    
    for cfg in SAMPLE_PDF_CONFIGS:
        # Generate sample PDF in sample_data/pdfs/
        pdf_path = generate_sample_pdf(cfg, settings.SAMPLE_DATA_DIR)
        
        # Also copy to uploads directory and index if not already present
        if cfg["filename"] not in existing_names:
            doc_id = f"demo_{Path(cfg['filename']).stem.lower()}"
            dest_path = settings.UPLOAD_DIR / f"{doc_id}_{cfg['filename']}"
            
            with open(pdf_path, "rb") as src, open(dest_path, "wb") as dst:
                dst.write(src.read())
                
            file_size = os.path.getsize(dest_path)
            pages = PDFService.extract_text_with_pages(str(dest_path))
            chunks = PDFService.chunk_document(pages, doc_id, cfg["filename"])
            
            if chunks:
                vector_store.add_chunks(chunks)
                
            crud.create_document(
                doc_id=doc_id,
                filename=dest_path.name,
                original_name=cfg["filename"],
                file_path=str(dest_path),
                file_size=file_size,
                page_count=len(pages),
                chunk_count=len(chunks)
            )
            
            crud.log_activity(
                action_type="demo_seeded",
                description=f"Auto-indexed sample document: {cfg['filename']}",
                metadata={"doc_id": doc_id, "chunks": len(chunks)}
            )
            print(f"[UniMate] Indexed sample document: {cfg['filename']} ({len(chunks)} chunks)")
