import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(r"C:\Unimate_AI_Assisstanat\Academic_Documents")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Helper functions
def draw_rounded_rect(draw, box, radius, fill, outline, width=1):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, color='#475569', width=2, arrow_size=8):
    import math
    x0, y0 = start
    x1, y1 = end
    draw.line([x0, y0, x1, y1], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    angle1 = angle + math.pi * 0.85
    angle2 = angle - math.pi * 0.85
    p1 = (x1 + arrow_size * math.cos(angle1), y1 + arrow_size * math.sin(angle1))
    p2 = (x1 + arrow_size * math.cos(angle2), y1 + arrow_size * math.sin(angle2))
    draw.polygon([end, p1, p2], fill=color)

# Fonts
try:
    f_title = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 22)
    f_sub = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 13)
    f_h2 = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 15)
    f_bold = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 12)
    f_body = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 11)
    f_sm = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 10)
    f_lbl = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 10)
except Exception:
    f_title = f_sub = f_h2 = f_bold = f_body = f_sm = f_lbl = ImageFont.load_default()

# -------------------------------------------------------------------
# 1. OVERALL SYSTEM ARCHITECTURE DIAGRAM
# -------------------------------------------------------------------
def create_architecture_diagram():
    W, H = 1500, 850
    img = Image.new("RGB", (W, H), color="#ffffff")
    draw = ImageDraw.Draw(img)

    # Outer border & header
    draw.rectangle([5, 5, W - 5, H - 5], outline="#cbd5e1", width=2)
    draw.rectangle([5, 5, W - 5, 70], fill="#1e1b4b")
    draw.text((W // 2, 28), "UniMate: Overall System Architecture", fill="#ffffff", font=f_title, anchor="mm")
    draw.text((W // 2, 52), "Multi-Tier Enterprise Architecture Grounded in Local RAG & Large Language Models", fill="#c7d2fe", font=f_sub, anchor="mm")

    # Tier 1: Client Presentation Tier
    t1_box = [30, 90, W - 30, 220]
    draw_rounded_rect(draw, t1_box, radius=10, fill="#f8fafc", outline="#94a3b8", width=1)
    draw.text((45, 100), "TIER 1: PRESENTATION LAYER (React 18 Single-Page Application + Tailwind CSS)", fill="#1e293b", font=f_h2)

    modules = [
        ("Dashboard", "KPIs & Activity Audit", "#e0e7ff", "#4338ca"),
        ("AI Chatbot", "Multi-turn RAG Tutor", "#ede9fe", "#6d28d9"),
        ("My Documents", "PyMuPDF Ingestion & Status", "#e0f2fe", "#0369a1"),
        ("AI Summarizer", "7 Academic Modes", "#fce7f3", "#be185d"),
        ("Quiz Generator", "MCQs & Explanations", "#fef3c7", "#b45309"),
        ("Study Planner", "Interactive Timetable", "#dcfce7", "#15803d"),
        ("Analytics", "Recharts Progress Tracking", "#f3e8ff", "#7e22ce"),
        ("GenAI Concepts", "Interactive Theory Guide", "#ffedd5", "#c2410c"),
    ]
    x0 = 45
    card_w = 164
    card_h = 70
    y0 = 132
    for idx, (title, sub, bg, border) in enumerate(modules):
        cx = x0 + idx * (card_w + 14)
        draw_rounded_rect(draw, [cx, y0, cx + card_w, y0 + card_h], radius=8, fill=bg, outline=border, width=1)
        draw.text((cx + card_w // 2, y0 + 22), title, fill=border, font=f_bold, anchor="mm")
        draw.text((cx + card_w // 2, y0 + 48), sub, fill="#475569", font=f_sm, anchor="mm")

    # Connecting Arrow
    draw_arrow(draw, (W // 2, 220), (W // 2, 265), color="#4338ca", width=3)
    draw.text((W // 2 + 10, 240), "Asynchronous REST API (JSON / Multipart)", fill="#4338ca", font=f_lbl)

    # Tier 2: API Gateway & Controller Tier
    t2_box = [30, 265, W - 30, 395]
    draw_rounded_rect(draw, t2_box, radius=10, fill="#f8fafc", outline="#94a3b8", width=1)
    draw.text((45, 275), "TIER 2: API GATEWAY & CONTROLLER LAYER (FastAPI ASGI Web Framework)", fill="#1e293b", font=f_h2)

    api_comps = [
        ("CORS Security & Regex", "Origins: 127.0.0.1, localhost", 45, 305, 260, 70, "#f1f5f9", "#475569"),
        ("Routing Gateway", "/chat, /documents, /summarize, /quiz", 330, 305, 265, 70, "#e0e7ff", "#4338ca"),
        ("Target Document Resolver", "doc_resolver.py (Name / Alias Filter)", 620, 305, 275, 70, "#ede9fe", "#6d28d9"),
        ("SQLite ORM / Data Layer", "database.py & crud.py transactions", 920, 305, 255, 70, "#ecfdf5", "#047857"),
        ("Activity Audit Service", "Real-time user event logging", 1200, 305, 255, 70, "#fef3c7", "#b45309"),
    ]
    for title, sub, x, y, w, h, bg, border in api_comps:
        draw_rounded_rect(draw, [x, y, x + w, y + h], radius=8, fill=bg, outline=border, width=1)
        draw.text((x + w // 2, y + 25), title, fill=border, font=f_bold, anchor="mm")
        draw.text((x + w // 2, y + 50), sub, fill="#475569", font=f_sm, anchor="mm")

    # Connectors to Lower Tier
    draw_arrow(draw, (200, 395), (200, 445), color="#0369a1", width=3)
    draw.text((120, 415), "PDF Stream", fill="#0369a1", font=f_lbl)

    draw_arrow(draw, (757, 395), (757, 445), color="#6d28d9", width=3)
    draw.text((765, 415), "Query & Resolver", fill="#6d28d9", font=f_lbl)

    draw_arrow(draw, (1047, 395), (1047, 445), color="#047857", width=3)
    draw.text((965, 415), "CRUD Queries", fill="#047857", font=f_lbl)

    # Tier 3: Core Engines
    # 3A: Ingestion
    box3a = [30, 445, 450, 680]
    draw_rounded_rect(draw, box3a, radius=10, fill="#f0f9ff", outline="#0284c7", width=1)
    draw.text((45, 455), "3. DOCUMENT PROCESSING (PyMuPDF)", fill="#0369a1", font=f_bold)
    steps_3a = [
        ("• Multipart Validation:", "MIME check, size limit (<=25MB)"),
        ("• In-Memory Parsing:", "fitz.open(stream), zero file locks"),
        ("• Page Tracking:", "Sequential page numbering preserved"),
        ("• Overlapping Chunking:", "800 chars / 150 overlap (Sentence bounds)"),
        ("• Duplicate Safety:", "Replaces older versions without orphaned vectors"),
    ]
    for idx, (head, val) in enumerate(steps_3a):
        sy = 485 + idx * 36
        draw.text((50, sy), head, fill="#0c4a6e", font=f_bold)
        draw.text((50, sy + 16), val, fill="#475569", font=f_sm)

    # 3B: Storage (Center)
    box3b = [500, 445, 960, 680]
    draw_rounded_rect(draw, box3b, radius=10, fill="#f5f3ff", outline="#7c3aed", width=1)
    draw.text((515, 455), "4. EMBEDDINGS & DATA STORAGE TIER", fill="#5b21b6", font=f_bold)

    draw_rounded_rect(draw, [515, 485, 945, 540], radius=6, fill="#ffffff", outline="#a78bfa", width=1)
    draw.text((530, 500), "Sentence Transformers (all-MiniLM-L6-v2)", fill="#4c1d95", font=f_bold)
    draw.text((530, 520), "Generates 384-dimensional dense semantic vectors", fill="#6b7280", font=f_sm)

    draw_rounded_rect(draw, [515, 550, 945, 605], radius=6, fill="#ffffff", outline="#a78bfa", width=1)
    draw.text((530, 565), "ChromaDB (Persistent Vector Database)", fill="#4c1d95", font=f_bold)
    draw.text((530, 585), "HNSW Cosine Similarity | Metadata: doc_id, doc_name, page_no", fill="#6b7280", font=f_sm)

    draw_rounded_rect(draw, [515, 615, 945, 665], radius=6, fill="#ffffff", outline="#10b981", width=1)
    draw.text((530, 627), "SQLite Relational Database (unimate.db)", fill="#065f46", font=f_bold)
    draw.text((530, 645), "documents, conversations, messages, quizzes, study_plans", fill="#6b7280", font=f_sm)

    # 3C: Reasoning (Right)
    box3c = [1010, 445, W - 30, 680]
    draw_rounded_rect(draw, box3c, radius=10, fill="#fffbeb", outline="#d97706", width=1)
    draw.text((1025, 455), "5. COGNITIVE REASONING & LLM TIER", fill="#92400e", font=f_bold)

    draw_rounded_rect(draw, [1025, 485, W - 45, 540], radius=6, fill="#ffffff", outline="#fcd34d", width=1)
    draw.text((1040, 500), "Context Augmentation Engine", fill="#78350f", font=f_bold)
    draw.text((1040, 520), "Injects ground-truth passages into system prompt constraints", fill="#6b7280", font=f_sm)

    draw_rounded_rect(draw, [1025, 550, W - 45, 605], radius=6, fill="#ffffff", outline="#3b82f6", width=1)
    draw.text((1040, 565), "Google Gemini 1.5 Flash (Live Mode)", fill="#1e40af", font=f_bold)
    draw.text((1040, 585), "Fast foundational reasoning, strict zero-hallucination instruction", fill="#6b7280", font=f_sm)

    draw_rounded_rect(draw, [1025, 615, W - 45, 665], radius=6, fill="#ffffff", outline="#64748b", width=1)
    draw.text((1040, 627), "Local Semantic Synthesizer (Offline Fallback)", fill="#334155", font=f_bold)
    draw.text((1040, 645), "Structured academic headings & verified citations", fill="#6b7280", font=f_sm)

    # Arrows between 3A -> 3B -> 3C
    draw_arrow(draw, (450, 560), (500, 560), color="#0284c7", width=3)
    draw_arrow(draw, (960, 560), (1010, 560), color="#7c3aed", width=3)
    draw.text((455, 540), "Chunks", fill="#0284c7", font=f_lbl)
    draw.text((965, 540), "Retrieved", fill="#7c3aed", font=f_lbl)

    # Tier 4: Grounded Output (Bottom)
    t4_box = [30, 705, W - 30, 825]
    draw_rounded_rect(draw, t4_box, radius=10, fill="#ecfdf5", outline="#059669", width=2)
    draw_arrow(draw, (W // 2, 680), (W // 2, 705), color="#059669", width=3)

    draw.text((50, 718), "6. GROUNDED CITATION TRACEABILITY & VERIFIED ACADEMIC OUTPUTS", fill="#065f46", font=f_h2)
    draw.text((50, 745), "• Factually Grounded Answers: Derives responses strictly from top-k retrieved chunks, mitigating hallucination risks.", fill="#047857", font=f_body)
    draw.text((50, 768), "• Verifiable Page-Level Citations: Every answer references document name & page number (e.g., Computer_Science_Syllabus.pdf - Page 2).", fill="#047857", font=f_body)
    draw.text((50, 792), "• Document-Specific Isolation: Enforces metadata filtering (`doc_name`) to eliminate cross-document topic contamination.", fill="#047857", font=f_body)

    out_file = OUT_DIR / "UniMate_Architecture_Diagram.png"
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Architecture diagram saved to {out_file}")

# -------------------------------------------------------------------
# 2. RAG WORKFLOW DIAGRAM
# -------------------------------------------------------------------
def create_rag_workflow_diagram():
    W, H = 1500, 850
    img = Image.new("RGB", (W, H), color="#ffffff")
    draw = ImageDraw.Draw(img)

    # Outer border & header
    draw.rectangle([5, 5, W - 5, H - 5], outline="#cbd5e1", width=2)
    draw.rectangle([5, 5, W - 5, 70], fill="#0f172a")
    draw.text((W // 2, 28), "UniMate: Detailed Retrieval-Augmented Generation (RAG) Pipeline", fill="#ffffff", font=f_title, anchor="mm")
    draw.text((W // 2, 52), "Two-Phase Workflow: Offline Document Ingestion & Real-Time Query Answering", fill="#94a3b8", font=f_sub, anchor="mm")

    # PHASE 1: DOCUMENT INGESTION (Top Half)
    p1_box = [30, 90, W - 30, 420]
    draw_rounded_rect(draw, p1_box, radius=10, fill="#f8fafc", outline="#64748b", width=1)
    draw.text((45, 102), "PHASE 1: DOCUMENT INGESTION, CHUNKING & VECTOR INDEXING PIPELINE", fill="#0f172a", font=f_h2)

    ingest_boxes = [
        ("1. PDF Document Upload", "Student uploads university PDF\n(Syllabus, Notes, Regulations)\nValidated <= 25MB", 50, 135, 240, 100, "#e0f2fe", "#0284c7"),
        ("2. In-Memory PyMuPDF", "fitz.open(stream=bytes)\nValidates PDF structure\nZero Windows file locks", 335, 135, 240, 100, "#e0f2fe", "#0284c7"),
        ("3. Page Text Extraction", "Sequential page extraction\nCleans whitespaces\nPreserves page_number", 620, 135, 240, 100, "#e0f2fe", "#0284c7"),
        ("4. Overlapping Chunking", "800 characters sliding window\n150-char overlap\nPreserves sentence bounds", 905, 135, 240, 100, "#ede9fe", "#7c3aed"),
        ("5. Dense Vectorization", "all-MiniLM-L6-v2 Transformer\nMaps chunks to 384-dim\nnormalized dense vectors", 1190, 135, 255, 100, "#ede9fe", "#7c3aed"),
    ]

    for title, desc, x, y, w, h, bg, border in ingest_boxes:
        draw_rounded_rect(draw, [x, y, x + w, y + h], radius=8, fill=bg, outline=border, width=1)
        draw.text((x + w // 2, y + 20), title, fill=border, font=f_bold, anchor="mm")
        y_txt = y + 42
        for line in desc.split("\n"):
            draw.text((x + w // 2, y_txt), line, fill="#334155", font=f_sm, anchor="mm")
            y_txt += 16

    # Arrows connecting Phase 1 steps
    for idx in range(len(ingest_boxes) - 1):
        x_from = ingest_boxes[idx][2] + ingest_boxes[idx][4]
        y_from = ingest_boxes[idx][3] + ingest_boxes[idx][5] // 2
        x_to = ingest_boxes[idx + 1][2]
        y_to = ingest_boxes[idx + 1][3] + ingest_boxes[idx + 1][5] // 2
        draw_arrow(draw, (x_from, y_from), (x_to, y_to), color="#0284c7", width=2)

    # Storage Banner in Phase 1
    storage_box = [200, 260, 1300, 395]
    draw_rounded_rect(draw, storage_box, radius=8, fill="#ffffff", outline="#7c3aed", width=1)
    draw.text((220, 275), "Persistent Storage Operations", fill="#5b21b6", font=f_bold)
    draw_arrow(draw, (1317, 235), (1317, 280), color="#7c3aed", width=2)
    draw_arrow(draw, (1317, 280), (1250, 280), color="#7c3aed", width=2)

    draw.text((220, 305), "• ChromaDB Vector Store: Persistent collection indexed using HNSW graph algorithm with Cosine Distance metric.", fill="#334155", font=f_body)
    draw.text((220, 330), "• Chunk Metadata Enrichment: Every vector stores { doc_id, doc_name, page_number, chunk_index, char_count }.", fill="#334155", font=f_body)
    draw.text((220, 355), "• SQLite State Store: Records document file paths, upload timestamps, file sizes, page counts, and activity logs.", fill="#334155", font=f_body)

    # PHASE 2: REAL-TIME QUERY ANSWERING (Bottom Half)
    p2_box = [30, 440, W - 30, 825]
    draw_rounded_rect(draw, p2_box, radius=10, fill="#f8fafc", outline="#64748b", width=1)
    draw.text((45, 452), "PHASE 2: REAL-TIME QUERY RETRIEVAL, GROUNDING & LLM SYNTHESIS", fill="#0f172a", font=f_h2)

    query_boxes = [
        ("1. Student Query", "Student enters question\n(e.g., 'Explain grading\nregulations only')", 50, 490, 240, 110, "#ecfdf5", "#059669"),
        ("2. Target Resolution", "doc_resolver.py checks\nfor explicit filename\nor document aliases", 335, 490, 240, 110, "#ecfdf5", "#059669"),
        ("3. ChromaDB Query", "Converts query to 384D\nExecutes cosine search\nApplies metadata filter", 620, 490, 240, 110, "#f5f3ff", "#7c3aed"),
        ("4. Prompt Construction", "Assembles top-k passages\nInjects system directives:\n'Derive strictly from context'", 905, 490, 240, 110, "#fffbeb", "#d97706"),
        ("5. LLM Synthesis", "Google Gemini 1.5 Flash\n(or Local Synthesizer)\nSynthesizes Markdown response", 1190, 490, 255, 110, "#fffbeb", "#d97706"),
    ]

    for title, desc, x, y, w, h, bg, border in query_boxes:
        draw_rounded_rect(draw, [x, y, x + w, y + h], radius=8, fill=bg, outline=border, width=1)
        draw.text((x + w // 2, y + 20), title, fill=border, font=f_bold, anchor="mm")
        y_txt = y + 42
        for line in desc.split("\n"):
            draw.text((x + w // 2, y_txt), line, fill="#334155", font=f_sm, anchor="mm")
            y_txt += 16

    # Arrows connecting Phase 2 steps
    for idx in range(len(query_boxes) - 1):
        x_from = query_boxes[idx][2] + query_boxes[idx][4]
        y_from = query_boxes[idx][3] + query_boxes[idx][5] // 2
        x_to = query_boxes[idx + 1][2]
        y_to = query_boxes[idx + 1][3] + query_boxes[idx + 1][5] // 2
        draw_arrow(draw, (x_from, y_from), (x_to, y_to), color="#059669", width=2)

    # Output Card in Phase 2
    res_box = [200, 630, 1300, 800]
    draw_rounded_rect(draw, res_box, radius=8, fill="#ffffff", outline="#059669", width=2)
    draw_arrow(draw, (1317, 600), (1317, 640), color="#059669", width=2)
    draw_arrow(draw, (1317, 640), (1250, 640), color="#059669", width=2)

    draw.text((220, 645), "Final Synthesized Output Delivered to Student Interface", fill="#065f46", font=f_bold)
    draw.text((220, 675), "1. Structured Academic Explanation: Organized using clean Markdown headings, sub-points, and concrete examples.", fill="#334155", font=f_body)
    draw.text((220, 705), "2. Verifiable Source Citation Pills: Badges display exact Document Name and Page Number for every cited passage.", fill="#334155", font=f_body)
    draw.text((220, 735), "3. Multi-turn Conversational Memory: Full interaction history saved to SQLite conversations table for ongoing study sessions.", fill="#334155", font=f_body)
    draw.text((220, 765), "4. Non-Existent Document Notice: Returns clear notification if requested document is absent from the indexed library.", fill="#334155", font=f_body)

    out_file = OUT_DIR / "UniMate_RAG_Workflow.png"
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"RAG workflow diagram saved to {out_file}")

# -------------------------------------------------------------------
# 3. COMPREHENSIVE UML & SYSTEM DIAGRAMS
# -------------------------------------------------------------------
def create_uml_diagrams():
    W, H = 1600, 1100
    img = Image.new("RGB", (W, H), color="#ffffff")
    draw = ImageDraw.Draw(img)

    # Outer border & header
    draw.rectangle([5, 5, W - 5, H - 5], outline="#cbd5e1", width=2)
    draw.rectangle([5, 5, W - 5, 65], fill="#1e1b4b")
    draw.text((W // 2, 26), "UniMate: Comprehensive UML & System Architecture Models", fill="#ffffff", font=f_title, anchor="mm")
    draw.text((W // 2, 48), "Use Case Diagram | Sequence Diagram | Data Flow Diagram (DFD Level 1) | Database Entity-Relationship (ER) Model", fill="#c7d2fe", font=f_sub, anchor="mm")

    # 4 Quadrants:
    # Q1 (Top-Left): Use Case Diagram
    # Q2 (Top-Right): DFD Level 1
    # Q3 (Bottom-Left): Sequence Diagram
    # Q4 (Bottom-Right): Database ER Diagram

    q1 = [25, 80, 785, 560]
    q2 = [815, 80, 1575, 560]
    q3 = [25, 580, 785, 1075]
    q4 = [815, 580, 1575, 1075]

    for q, title, color in [(q1, "1. USE CASE DIAGRAM", "#4338ca"), 
                           (q2, "2. DATA FLOW DIAGRAM (DFD LEVEL 1)", "#0369a1"), 
                           (q3, "3. SYSTEM SEQUENCE DIAGRAM (RAG QUERY)", "#b45309"), 
                           (q4, "4. DATABASE ENTITY-RELATIONSHIP (ER) MODEL", "#047857")]:
        draw_rounded_rect(draw, q, radius=8, fill="#f8fafc", outline=color, width=1)
        draw.text((q[0] + 15, q[1] + 12), title, fill=color, font=f_h2)

    # --- Q1: Use Case Diagram ---
    # Actor: Student
    draw.ellipse([60, 150, 90, 180], fill="#ffffff", outline="#1e293b", width=2) # head
    draw.line([75, 180, 75, 230], fill="#1e293b", width=2) # torso
    draw.line([50, 200, 100, 200], fill="#1e293b", width=2) # arms
    draw.line([75, 230, 55, 270], fill="#1e293b", width=2) # leg L
    draw.line([75, 230, 95, 270], fill="#1e293b", width=2) # leg R
    draw.text((75, 285), "University\nStudent", fill="#1e293b", font=f_bold, anchor="mm")

    # Use Cases (Ellipses)
    use_cases = [
        ("UC-1: Upload & Manage University PDFs", 130),
        ("UC-2: Ask Conversational RAG Questions", 185),
        ("UC-3: Filter Retrieval by Document Name", 240),
        ("UC-4: Generate Multi-Format Notes Summaries", 295),
        ("UC-5: Generate & Solve Practice Quizzes", 350),
        ("UC-6: Create & Track Daily Study Plans", 405),
        ("UC-7: View Learning Analytics & Audit Trails", 460),
        ("UC-8: Explore GenAI Foundations & Architectures", 515),
    ]
    for text, y in use_cases:
        draw_rounded_rect(draw, [200, y - 16, 750, y + 16], radius=15, fill="#ffffff", outline="#4338ca", width=1)
        draw.text((475, y), text, fill="#1e1b4b", font=f_body, anchor="mm")
        draw.line([105, 210, 200, y], fill="#94a3b8", width=1)

    # --- Q2: Data Flow Diagram (DFD Level 1) ---
    dfd_nodes = [
        ("Student Client", 840, 150, 140, 50, "#e0e7ff", "#4338ca"),
        ("1.0 Upload Engine", 1040, 120, 170, 50, "#e0f2fe", "#0284c7"),
        ("2.0 PyMuPDF Parser", 1300, 120, 180, 50, "#e0f2fe", "#0284c7"),
        ("3.0 ChromaDB Store", 1300, 240, 180, 50, "#f5f3ff", "#7c3aed"),
        ("4.0 RAG Query Engine", 1040, 240, 170, 50, "#ede9fe", "#6d28d9"),
        ("5.0 Gemini 1.5 LLM", 1040, 370, 170, 50, "#fffbeb", "#d97706"),
        ("6.0 SQLite Database", 1300, 370, 180, 50, "#ecfdf5", "#047857"),
    ]
    for name, x, y, w, h, bg, border in dfd_nodes:
        draw_rounded_rect(draw, [x, y, x + w, y + h], radius=6, fill=bg, outline=border, width=1)
        draw.text((x + w // 2, y + h // 2), name, fill=border, font=f_bold, anchor="mm")

    # DFD Flow arrows
    draw_arrow(draw, (980, 160), (1040, 145), color="#0284c7", width=2) # Student -> Upload
    draw_arrow(draw, (1210, 145), (1300, 145), color="#0284c7", width=2) # Upload -> PyMuPDF
    draw_arrow(draw, (1390, 170), (1390, 240), color="#7c3aed", width=2) # PyMuPDF -> ChromaDB
    draw_arrow(draw, (980, 185), (1040, 255), color="#6d28d9", width=2) # Student -> RAG
    draw_arrow(draw, (1300, 265), (1210, 265), color="#7c3aed", width=2) # ChromaDB -> RAG
    draw_arrow(draw, (1125, 290), (1125, 370), color="#d97706", width=2) # RAG -> Gemini
    draw_arrow(draw, (1210, 395), (1300, 395), color="#047857", width=2) # Gemini/RAG -> SQLite
    draw_arrow(draw, (1040, 275), (980, 195), color="#059669", width=2) # RAG -> Student

    draw.text((990, 125), "PDF File", fill="#0284c7", font=f_sm)
    draw.text((1225, 125), "Text Stream", fill="#0284c7", font=f_sm)
    draw.text((1400, 205), "384D Vectors", fill="#7c3aed", font=f_sm)
    draw.text((990, 235), "Natural Query", fill="#6d28d9", font=f_sm)
    draw.text((1220, 245), "Retrieved Chunks", fill="#7c3aed", font=f_sm)
    draw.text((1135, 325), "Grounded Prompt", fill="#d97706", font=f_sm)
    draw.text((1220, 410), "Log & State", fill="#047857", font=f_sm)

    # --- Q3: Sequence Diagram ---
    seq_actors = ["Student", "React UI", "FastAPI Router", "ChromaDB", "Gemini 1.5"]
    seq_xs = [65, 215, 385, 555, 715]
    
    for name, x in zip(seq_actors, seq_xs):
        draw_rounded_rect(draw, [x - 45, 625, x + 45, 655], radius=4, fill="#ffffff", outline="#475569", width=1)
        draw.text((x, 640), name, fill="#1e293b", font=f_bold, anchor="mm")
        draw.line([x, 655, x, 1045], fill="#cbd5e1", width=1) # lifeline

    seq_messages = [
        (0, 1, 680, "1: Submit Question", "#1e293b"),
        (1, 2, 720, "2: POST /api/chat/message", "#4338ca"),
        (2, 2, 760, "3: doc_resolver(query)", "#6d28d9"),
        (2, 3, 800, "4: query(vector, where=doc_name)", "#7c3aed"),
        (3, 2, 840, "5: Return top-k chunks + page_no", "#7c3aed"),
        (2, 4, 880, "6: generate_content(context + query)", "#d97706"),
        (4, 2, 920, "7: Synthesized Grounded Response", "#d97706"),
        (2, 2, 960, "8: Save message & activity log", "#047857"),
        (2, 1, 1000, "9: JSON { answer, sources, engine }", "#4338ca"),
        (1, 0, 1030, "10: Render Markdown + Citations", "#059669"),
    ]
    for frm, to, y, msg, col in seq_messages:
        x_from = seq_xs[frm]
        x_to = seq_xs[to]
        if x_from == x_to:
            draw.line([x_from, y - 5, x_from + 30, y - 5], fill=col, width=1)
            draw.line([x_from + 30, y - 5, x_from + 30, y + 10], fill=col, width=1)
            draw_arrow(draw, (x_from + 30, y + 10), (x_from, y + 10), color=col, width=1)
            draw.text((x_from + 35, y + 2), msg, fill=col, font=f_sm)
        else:
            draw_arrow(draw, (x_from, y), (x_to, y), color=col, width=1)
            draw.text(((x_from + x_to) // 2, y - 10), msg, fill=col, font=f_sm, anchor="mm")

    # --- Q4: Database ER Diagram ---
    er_tables = [
        ("documents", 840, 625, 210, 120, [
            ("id (PK)", "VARCHAR(36)"),
            ("filename", "TEXT"),
            ("original_name", "TEXT"),
            ("page_count", "INTEGER"),
            ("chunk_count", "INTEGER"),
            ("upload_date", "TIMESTAMP"),
        ], "#0284c7"),
        ("conversations", 1100, 625, 200, 95, [
            ("id (PK)", "VARCHAR(36)"),
            ("title", "TEXT"),
            ("created_at", "TIMESTAMP"),
            ("updated_at", "TIMESTAMP"),
        ], "#7c3aed"),
        ("messages", 1340, 625, 215, 120, [
            ("id (PK)", "VARCHAR(36)"),
            ("conversation_id (FK)", "VARCHAR(36)"),
            ("sender", "TEXT"),
            ("content", "TEXT"),
            ("sources", "TEXT (JSON)"),
            ("created_at", "TIMESTAMP"),
        ], "#7c3aed"),
        ("quizzes", 840, 785, 210, 125, [
            ("id (PK)", "VARCHAR(36)"),
            ("topic", "TEXT"),
            ("difficulty", "TEXT"),
            ("num_questions", "INTEGER"),
            ("score", "INTEGER"),
            ("data", "TEXT (JSON)"),
        ], "#b45309"),
        ("study_plans", 1100, 785, 200, 110, [
            ("id (PK)", "VARCHAR(36)"),
            ("subject", "TEXT"),
            ("daily_hours", "REAL"),
            ("exam_date", "TEXT"),
            ("total_topics", "INTEGER"),
        ], "#047857"),
        ("study_topics", 1340, 785, 215, 110, [
            ("id (PK)", "VARCHAR(36)"),
            ("plan_id (FK)", "VARCHAR(36)"),
            ("day_number", "INTEGER"),
            ("topic_name", "TEXT"),
            ("is_completed", "BOOLEAN"),
        ], "#047857"),
        ("activity_logs", 1080, 935, 240, 100, [
            ("id (PK)", "INTEGER AUTO"),
            ("action_type", "TEXT"),
            ("description", "TEXT"),
            ("created_at", "TIMESTAMP"),
        ], "#475569"),
    ]

    for tbl_name, tx, ty, tw, th, fields, hdr_col in er_tables:
        draw_rounded_rect(draw, [tx, ty, tx + tw, ty + th], radius=6, fill="#ffffff", outline=hdr_col, width=1)
        draw.rectangle([tx, ty, tx + tw, ty + 22], fill=hdr_col)
        draw.text((tx + tw // 2, ty + 11), tbl_name, fill="#ffffff", font=f_bold, anchor="mm")
        fy = ty + 28
        for fname, ftype in fields:
            draw.text((tx + 6, fy), fname, fill="#1e293b", font=f_sm)
            draw.text((tx + tw - 6, fy), ftype, fill="#64748b", font=f_sm, anchor="ra")
            fy += 15

    # ER Relationship lines
    # conversations 1 -> N messages
    draw.line([1300, 670, 1340, 670], fill="#7c3aed", width=2)
    draw.text((1305, 655), "1", fill="#7c3aed", font=f_bold)
    draw.text((1330, 655), "N", fill="#7c3aed", font=f_bold)

    # study_plans 1 -> N study_topics
    draw.line([1300, 840, 1340, 840], fill="#047857", width=2)
    draw.text((1305, 825), "1", fill="#047857", font=f_bold)
    draw.text((1330, 825), "N", fill="#047857", font=f_bold)

    out_file = OUT_DIR / "UniMate_UML_Diagrams.png"
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"UML diagrams saved to {out_file}")

if __name__ == "__main__":
    create_architecture_diagram()
    create_rag_workflow_diagram()
    create_uml_diagrams()
    print("All diagrams generated successfully!")
