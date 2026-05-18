from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db

from app.services.dashboard_service import (
    summary_service,
    task_distribution_service,
    approvals_service,
    ai_summary_service,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return summary_service(
        db,
        user,
    )


@router.get("/task-distribution")
def task_distribution(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return task_distribution_service(
        db,
        user,
    )


@router.get("/approvals")
def approvals(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return approvals_service(
        db,
        user,
    )


@router.get("/ai-summary")
def ai_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return ai_summary_service(
        db,
        user,
    )