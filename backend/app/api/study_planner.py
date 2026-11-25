import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Union
from backend.app.services.gemini_service import gemini_service
from backend.app.database import crud

router = APIRouter(prefix="/study-planner", tags=["Study Planner"])

class StudyPlanRequest(BaseModel):
    subject: str
    topics: Union[List[str], str]
    daily_hours: float = 2.5
    exam_date: str
    difficulty: str = "Medium"

class ToggleTopicRequest(BaseModel):
    completed: bool

@router.post("/generate")
def create_study_plan(req: StudyPlanRequest):
    # Parse topics if provided as string
    if isinstance(req.topics, str):
        topic_list = [t.strip() for t in req.topics.split(",") if t.strip()]
    else:
        topic_list = [t.strip() for t in req.topics if t.strip()]
        
    if not topic_list:
        raise HTTPException(status_code=400, detail="Please provide at least one topic to study.")
        
    schedule = gemini_service.generate_study_plan(
        subject=req.subject,
        topics=topic_list,
        daily_hours=req.daily_hours,
        exam_date=req.exam_date,
        difficulty=req.difficulty
    )
    
    plan_id = str(uuid.uuid4())
    crud.save_study_plan(
        plan_id=plan_id,
        subject=req.subject,
        exam_date=req.exam_date,
        daily_hours=req.daily_hours,
        difficulty=req.difficulty,
        topics=topic_list,
        schedule=schedule
    )
    
    crud.log_activity(
        action_type="study_plan_created",
        description=f"Created study timetable for '{req.subject}' ({len(schedule)} days)",
        metadata={"plan_id": plan_id, "subject": req.subject}
    )
    
    return {
        "plan_id": plan_id,
        "subject": req.subject,
        "exam_date": req.exam_date,
        "daily_hours": req.daily_hours,
        "schedule": schedule
    }

@router.get("/plans")
def list_study_plans():
    return crud.get_all_study_plans()

@router.get("/plan/{plan_id}/topics")
def get_plan_topics(plan_id: str):
    return crud.get_study_topics_status(plan_id)

@router.post("/topic/{topic_id}/toggle")
def toggle_topic(topic_id: str, req: ToggleTopicRequest):
    crud.toggle_topic_completion(topic_id, req.completed)
    status_str = "Completed" if req.completed else "Marked pending"
    crud.log_activity(
        action_type="study_topic_toggled",
        description=f"{status_str} study topic"
    )
    return {"topic_id": topic_id, "completed": req.completed}
