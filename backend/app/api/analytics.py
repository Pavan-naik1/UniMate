from fastapi import APIRouter
from backend.app.database import crud
from backend.app.rag.vector_store import vector_store
from backend.app.services.gemini_service import gemini_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview")
def get_analytics():
    metrics = crud.get_analytics_metrics()
    activities = crud.get_recent_activities(limit=10)
    chroma_stats = vector_store.get_stats()
    gemini_status = gemini_service.check_status()
    
    # Format quiz trend data for Recharts
    quiz_trend_data = []
    for q in metrics.get("quiz_scores", []):
        quiz_trend_data.append({
            "name": q.get("title", "Quiz")[:14],
            "score": round(q.get("percentage", 0), 1),
            "date": q.get("completed_at", "")[:10]
        })
        
    return {
        "metrics": metrics,
        "recent_activities": activities,
        "quiz_chart_data": quiz_trend_data,
        "vector_store_stats": chroma_stats,
        "ai_engine_status": gemini_status
    }
