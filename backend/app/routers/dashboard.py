from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.services.dashboard_service import get_approval_stats, get_dashboard_summary, get_task_distribution

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_dashboard_summary(user, db)


@router.get("/task-distribution")
def task_distribution(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_task_distribution(user, db)


@router.get("/approvals")
def approvals(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_approval_stats(db)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.task import Task
from app.services.ai_service import generate_ai_summary


# @router.get("/ai-summary")
# def ai_summary(db: Session = Depends(get_db)):
#     tasks = db.query(Task).all()
#     return generate_ai_summary(tasks)