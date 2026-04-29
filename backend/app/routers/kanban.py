from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.task import TaskOut, TaskStatusUpdate
from app.services.kanban_service import get_kanban_board, update_task_status

router = APIRouter(prefix="/kanban", tags=["Kanban"])


@router.patch("/tasks/{task_id}/status", response_model=TaskOut)
def change_status(
    task_id: int,
    payload: TaskStatusUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return update_task_status(task_id, payload.status, user, db)


@router.get("/board")
def get_board(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return get_kanban_board(user, db)
