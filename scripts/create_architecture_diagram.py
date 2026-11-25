import os
from PIL import Image, ImageDraw, ImageFont

def draw_rounded_rect(draw, box, radius, fill, outline, width=1):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, color='#475569', width=2, arrow_size=8):
    x0, y0 = start
    x1, y1 = end
    draw.line([x0, y0, x1, y1], fill=color, width=width)
    
    # Draw arrow head
    import math
    angle = math.atan2(y1 - y0, x1 - x0)
    angle1 = angle + math.pi * 0.85
    angle2 = angle - math.pi * 0.85
    
    p1 = (x1 + arrow_size * math.cos(angle1), y1 + arrow_size * math.sin(angle1))
    p2 = (x1 + arrow_size * math.cos(angle2), y1 + arrow_size * math.sin(angle2))
    draw.polygon([end, p1, p2], fill=color)

def generate_diagram(output_path="architecture_diagram.png"):
    W, H = 1400, 800
    img = Image.new("RGB", (W, H), color="#ffffff")
    draw = ImageDraw.Draw(img)

    # Load Windows fonts
    try:
        f_title = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 22)
        f_sub = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 13)
        f_tier = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_box_title = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 13)
        f_box_text = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 11)
        f_lbl = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 10)
    except Exception:
        f_title = f_sub = f_tier = f_box_title = f_box_text = f_lbl = ImageFont.load_default()

    # Outer border
    draw.rectangle([5, 5, W - 5, H - 5], outline="#cbd5e1", width=2)

    # Header Banner
    draw.rectangle([5, 5, W - 5, 65], fill="#1e1b4b")
    draw.text((W // 2, 26), "UniMate: System Architecture & Data Flow Diagram", fill="#ffffff", font=f_title, anchor="mm")
    draw.text((W // 2, 50), "End-to-End Pipeline: Client Presentation -> FastAPI Gateway -> RAG Ingestion -> ChromaDB Vector Store -> LLM Reasoning", fill="#c7d2fe", font=f_sub, anchor="mm")

    # ================= TIER 1: Presentation Tier (Top) =================
    tier1_box = [30, 85, W - 30, 210]
    draw_rounded_rect(draw, tier1_box, radius=10, fill="#f8fafc", outline="#94a3b8", width=1)
    draw.text((45, 95), "1. CLIENT PRESENTATION TIER (React 18 + Vite + Tailwind CSS)", fill="#1e293b", font=f_tier)

    # Modules in Tier 1
    t1_modules = [
        ("Dashboard", "KPIs & Quick Actions", "#e0e7ff", "#4338ca"),
        ("AI Chatbot", "Multi-turn RAG Chat", "#ede9fe", "#6d28d9"),
        ("My Documents", "Upload & ChromaDB Status", "#e0f2fe", "#0369a1"),
        ("AI Summarizer", "7 Academic Modes", "#fce7f3", "#be185d"),
        ("Quiz Generator", "MCQs & Explanations", "#fef3c7", "#b45309"),
        ("Study Planner", "Interactive Timetable", "#dcfce7", "#15803d"),
        ("Analytics", "Progress & Metrics", "#f3e8ff", "#7e22ce"),
        ("GenAI Concepts", "Interactive Theory Guide", "#ffedd5", "#c2410c"),
    ]

    x_start = 45
    card_w = 152
    card_h = 70
    y_card = 125

    for idx, (title, sub, bg, border) in enumerate(t1_modules):
        cx = x_start + idx * (card_w + 14)
        draw_rounded_rect(draw, [cx, y_card, cx + card_w, y_card + card_h], radius=8, fill=bg, outline=border, width=1)
        draw.text((cx + card_w // 2, y_card + 22), title, fill=border, font=f_box_title, anchor="mm")
        draw.text((cx + card_w // 2, y_card + 48), sub, fill="#475569", font=f_box_text, anchor="mm")

    # Arrow Down to Tier 2
    draw_arrow(draw, (W // 2, 210), (W // 2, 255), color="#4338ca", width=3)
    draw.text((W // 2 + 10, 230), "REST API Calls (JSON / Multipart)", fill="#4338ca", font=f_lbl)

    # ================= TIER 2: API Gateway Tier (Middle) =================
    tier2_box = [30, 255, W - 30, 375]
    draw_rounded_rect(draw, tier2_box, radius=10, fill="#f8fafc", outline="#94a3b8", width=1)
    draw.text((45, 265), "2. API GATEWAY & CONTROLLER TIER (FastAPI ASGI Framework)", fill="#1e293b", font=f_tier)

    t2_components = [
        ("CORS Middleware", "Origin Validation & Regex", 45, 295, 240, 65, "#f1f5f9", "#475569"),
        ("Router Gateway", "/chat, /docs, /quiz, /plan", 305, 295, 240, 65, "#e0e7ff", "#4338ca"),
        ("Doc Target Resolver", "doc_resolver.py (Name Filter)", 565, 295, 245, 65, "#ede9fe", "#6d28d9"),
        ("SQLite ORM / CRUD", "State & Transaction Mgr", 830, 295, 240, 65, "#ecfdf5", "#047857"),
        ("Activity Auditor", "Real-time Action Logging", 1090, 295, 265, 65, "#fef3c7", "#b45309"),
    ]

    for title, sub, x, y, w, h, bg, border in t2_components:
        draw_rounded_rect(draw, [x, y, x + w, y + h], radius=8, fill=bg, outline=border, width=1)
        draw.text((x + w // 2, y + 22), title, fill=border, font=f_box_title, anchor="mm")
        draw.text((x + w // 2, y + 46), sub, fill="#475569", font=f_box_text, anchor="mm")

    # Branching arrows from Tier 2 to Lower Tiers
    # Arrow to Ingestion (Left)
    draw_arrow(draw, (200, 375), (200, 425), color="#0369a1", width=3)
    draw.text((120, 395), "PDF Stream", fill="#0369a1", font=f_lbl)

    # Arrow to SQLite (Center Left)
    draw_arrow(draw, (950, 375), (950, 425), color="#047857", width=3)
    draw.text((875, 395), "CRUD Queries", fill="#047857", font=f_lbl)

    # Arrow to RAG Reasoning (Right)
    draw_arrow(draw, (685, 375), (685, 425), color="#6d28d9", width=3)
    draw.text((695, 395), "Chat Query", fill="#6d28d9", font=f_lbl)

    # ================= TIER 3: Lower Subsystems =================

    # Box 3A: Document Ingestion Pipeline (Left)
    box3a = [30, 425, 430, 640]
    draw_rounded_rect(draw, box3a, radius=10, fill="#f0f9ff", outline="#0284c7", width=1)
    draw.text((45, 435), "3. DOCUMENT PROCESSING (PyMuPDF)", fill="#0369a1", font=f_box_title)
    
    ingest_steps = [
        ("1. Multipart Ingestion", "Type check, size validation (<=25MB)"),
        ("2. In-Memory PyMuPDF", "fitz.open(stream), zero file locks"),
        ("3. Page Preservation", "Text extracted with exact page numbers"),
        ("4. Overlapping Chunking", "800 chars / 150 overlap (Sentence bounds)"),
        ("5. Duplicate Safety", "Replaces older versions cleanly"),
    ]
    for idx, (st, desc) in enumerate(ingest_steps):
        sy = 465 + idx * 33
        draw.text((50, sy), st, fill="#0c4a6e", font=f_box_title)
        draw.text((50, sy + 15), desc, fill="#475569", font=f_box_text)

    # Arrow from Ingestion to Vector DB
    draw_arrow(draw, (430, 530), (480, 530), color="#0284c7", width=3)
    draw.text((435, 510), "Chunks", fill="#0284c7", font=f_lbl)

    # Box 3B: Vector & Relational Storage Tier (Center)
    box3b = [480, 425, 900, 640]
    draw_rounded_rect(draw, box3b, radius=10, fill="#f5f3ff", outline="#7c3aed", width=1)
    draw.text((495, 435), "4. EMBEDDINGS & STORAGE TIER", fill="#5b21b6", font=f_box_title)

    # Sub-component: Sentence Transformers
    draw_rounded_rect(draw, [495, 465, 885, 515], radius=6, fill="#ffffff", outline="#a78bfa", width=1)
    draw.text((510, 480), "Sentence Transformers (all-MiniLM-L6-v2)", fill="#4c1d95", font=f_box_title)
    draw.text((510, 498), "384-Dimensional Dense Numerical Embeddings", fill="#6b7280", font=f_box_text)

    # Sub-component: ChromaDB
    draw_rounded_rect(draw, [495, 525, 885, 575], radius=6, fill="#ffffff", outline="#a78bfa", width=1)
    draw.text((510, 540), "ChromaDB (Persistent Vector Store)", fill="#4c1d95", font=f_box_title)
    draw.text((510, 558), "HNSW Cosine Search | Metadata: doc_name, page_number", fill="#6b7280", font=f_box_text)

    # Sub-component: SQLite
    draw_rounded_rect(draw, [495, 585, 885, 630], radius=6, fill="#ffffff", outline="#10b981", width=1)
    draw.text((510, 597), "SQLite Database (unimate.db)", fill="#065f46", font=f_box_title)
    draw.text((510, 613), "documents, conversations, messages, quizzes, study_plans", fill="#6b7280", font=f_box_text)

    # Arrow from Vector DB to LLM Reasoning
    draw_arrow(draw, (900, 530), (950, 530), color="#7c3aed", width=3)
    draw.text((903, 510), "Retrieved Chunks", fill="#7c3aed", font=f_lbl)

    # Box 3C: Cognitive Reasoning & LLM Tier (Right)
    box3c = [950, 425, W - 30, 640]
    draw_rounded_rect(draw, box3c, radius=10, fill="#fffbeb", outline="#d97706", width=1)
    draw.text((965, 435), "5. COGNITIVE REASONING & LLM TIER", fill="#92400e", font=f_box_title)

    # Sub-component: Grounded Prompt Engine
    draw_rounded_rect(draw, [965, 465, W - 45, 515], radius=6, fill="#ffffff", outline="#fcd34d", width=1)
    draw.text((980, 480), "Context-Aware Prompt Construction", fill="#78350f", font=f_box_title)
    draw.text((980, 498), "System constraints, ground-truth passages injected", fill="#6b7280", font=f_box_text)

    # Sub-component: Gemini 1.5 Flash (Live)
    draw_rounded_rect(draw, [965, 525, W - 45, 575], radius=6, fill="#ffffff", outline="#3b82f6", width=1)
    draw.text((980, 540), "Google Gemini 1.5 Flash API (Live Mode)", fill="#1e40af", font=f_box_title)
    draw.text((980, 558), "Fast multi-turn reasoning, zero-hallucination instruction", fill="#6b7280", font=f_box_text)

    # Sub-component: Local Synthesizer (Fallback)
    draw_rounded_rect(draw, [965, 585, W - 45, 630], radius=6, fill="#ffffff", outline="#64748b", width=1)
    draw.text((980, 597), "Local Semantic Synthesizer (Offline Engine)", fill="#334155", font=f_box_title)
    draw.text((980, 613), "Structured academic headings & verified citations", fill="#6b7280", font=f_box_text)

    # ================= TIER 4: Verified Output Banner (Bottom) =================
    tier4_box = [30, 665, W - 30, 775]
    draw_rounded_rect(draw, tier4_box, radius=10, fill="#ecfdf5", outline="#059669", width=2)
    
    # Arrow Down to Tier 4
    draw_arrow(draw, (W // 2, 640), (W // 2, 665), color="#059669", width=3)

    draw.text((50, 680), "6. VERIFIED GROUNDED OUTPUT & CITATION TRACEABILITY", fill="#065f46", font=f_tier)
    
    draw.text((50, 710), "- High-Quality Academic Answers: Formatted in structured Markdown with core concepts, academic breakdowns, and exam tips.", fill="#047857", font=f_box_text)
    draw.text((50, 730), "- Verifiable Citations: Every answer references the source document name and exact page number (e.g., Computer_Science_Syllabus.pdf - Page 2).", fill="#047857", font=f_box_text)
    draw.text((50, 750), "- Zero Hallucination Guarantee: Chunks strictly filtered via ChromaDB metadata; if absent, user receives explicit notification.", fill="#047857", font=f_box_text)

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Diagram saved successfully at {output_path}")

if __name__ == "__main__":
    generate_diagram("architecture_diagram.png")
