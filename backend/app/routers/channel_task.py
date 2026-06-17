from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import Page

from app.db.database import get_db

from app.core.dependencies import (
    get_current_user,
)

from app.models.user import User

from app.schemas.task import (
    TaskCreate,
    TaskAssign,
    TaskOut,
)

from app.services.task_service import (
    create_task_service,
    assign_task_service,
)

from app.repository.task_repository import (
    TaskRepository,
)

router = APIRouter(
    prefix="/channels",
    tags=["Channel Tasks"],
)


@router.post(
    "/{channel_id}/tasks",
    response_model=TaskOut,
)
def create_channel_task(
    channel_id: int,
    workspace_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):

    return create_task_service(
        db=db,
        current_user=current_user,
        task=payload,
        workspace_id=workspace_id,
        channel_id=channel_id,
    )


@router.get(
    "/{channel_id}/tasks",
    response_model=Page[TaskOut],
)
def list_channel_tasks(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):

    return TaskRepository.list_channel_tasks(
        db=db,
        channel_id=channel_id,
    )


@router.get(
    "/{channel_id}/tasks/{task_id}",
    response_model=TaskOut,
)
def get_channel_task(
    channel_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):

    return TaskRepository.get_channel_task(
        db=db,
        channel_id=channel_id,
        task_id=task_id,
    )


@router.patch(
    "/{channel_id}/tasks/{task_id}/assign",
    response_model=TaskOut,
)
def assign_channel_task(
    channel_id: int,
    task_id: int,
    payload: TaskAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):

    return assign_task_service(
        db=db,
        current_user=current_user,
        task_id=task_id,
        assignment=payload,
    )