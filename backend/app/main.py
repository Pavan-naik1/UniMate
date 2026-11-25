import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.core.config import settings
from backend.app.database.database import init_db
from backend.app.api import chat, documents, summarizer, quiz, study_planner, analytics, genai_concepts
from backend.app.utils.sample_generator import seed_sample_documents_if_needed
from backend.app.services.gemini_service import gemini_service

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="UniMate: An Intelligent University Assistant Using Generative AI and Large Language Models"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all API routers
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(summarizer.router, prefix=settings.API_V1_STR)
app.include_router(quiz.router, prefix=settings.API_V1_STR)
app.include_router(study_planner.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(genai_concepts.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def on_startup():
    print(f"==================================================")
    print(f" Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"==================================================")
    
    # 1. Initialize SQLite Database
    init_db()
    print("✓ SQLite database initialized at:", settings.DATABASE_PATH)
    
    # 2. Seed Sample PDFs and Auto-Index in ChromaDB
    try:
        seed_sample_documents_if_needed()
        print("✓ Sample university PDFs indexed in ChromaDB.")
    except Exception as e:
        print(f"! Notice: Sample seeding had non-critical issue: {e}")
        
    # 3. Check Gemini AI Engine Status
    status = gemini_service.check_status()
    if status["live_mode"]:
        print(f"✓ AI Engine: Live Gemini ({status['model']})")
    else:
        print("✓ AI Engine: Local Semantic RAG Engine active (Gemini key can be added in .env)")
        
    print(f"UniMate Backend ready at http://localhost:8000")

@app.get("/api/health")
def health_check():
    ai_status = gemini_service.check_status()
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "ai_engine": ai_status
    }

# Mount static frontend build if it exists
frontend_dist = settings.BASE_DIR / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
