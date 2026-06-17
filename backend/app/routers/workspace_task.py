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
    prefix="/workspaces",
    tags=["Workspace Tasks"],
)


@router.post(
    "/{workspace_id}/tasks",
    response_model=TaskOut,
)
def create_workspace_task(
    workspace_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    return create_task_service(
        db=db,
        current_user=current_user,
        task=payload,
        workspace_id=workspace_id,
        channel_id=None,
    )


@router.get(
    "/{workspace_id}/tasks",
    response_model=Page[TaskOut],
)
def list_workspace_tasks(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    return TaskRepository.list_workspace_tasks(
        db=db,
        workspace_id=workspace_id,
    )


@router.get(
    "/{workspace_id}/tasks/{task_id}",
    response_model=TaskOut,
)
def get_workspace_task(
    workspace_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    return TaskRepository.get_workspace_task(
        db=db,
        workspace_id=workspace_id,
        task_id=task_id,
    )


@router.patch(
    "/{workspace_id}/tasks/{task_id}/assign",
    response_model=TaskOut,
)
def assign_workspace_task(
    workspace_id: int,
    task_id: int,
    payload: TaskAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    return assign_task_service(
        db=db,
        current_user=current_user,
        task_id=task_id,
        assignment=payload,
    )