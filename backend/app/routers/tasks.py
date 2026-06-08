from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.core.permissions import get_current_user, require_roles
from app.db.database import get_db

from app.models.user import User

from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskOut,
    TaskAssign,
    TaskStatusUpdate,
)

from app.services.task_service import (
    create_task_service,
    create_task_with_document_service,
    list_tasks_service,
    get_task_service,
    update_task_service,
    delete_task_service,
    update_task_status_service,
    assign_task_service,
    smart_assign_task_service,
    kanban_service,
    recommendation_service,
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

MANAGEMENT_ROLES = [
    "organization_admin",
    "workspace_admin",
    "manager",
]


@router.post(
    "/",
    response_model=TaskOut,
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(MANAGEMENT_ROLES)
    ),
):
    return create_task_service(
        db,
        current_user,
        task,
    )


@router.post(
    "/withdocument",
    response_model=TaskOut,
)
def create_task_with_document(
    title: str = Form(...),
    description: str = Form(...),
    status_value: str = Form(...),
    priority: str = Form(...),
    due_date: str = Form(None),
    assigned_to_id: int = Form(None),
    document: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(MANAGEMENT_ROLES)
    ),
):
    return create_task_with_document_service(
        db=db,
        current_user=current_user,
        title=title,
        description=description,
        status_value=status_value,
        priority=priority,
        due_date=due_date,
        assigned_to_id=assigned_to_id,
        document=document,
    )


@router.get(
    "/",
    response_model=Page[TaskOut],
)
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_tasks_service(
        db,
        current_user,
    )


@router.get("/kanban")
def get_kanban(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return kanban_service(
        db,
        current_user,
    )


@router.get("/assignment/recommendation")
def assignment_recommendation(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(MANAGEMENT_ROLES)
    ),
):
    return recommendation_service(
        db,
        current_user,
    )


@router.get(
    "/{task_id}",
    response_model=TaskOut,
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_task_service(
        db,
        current_user,
        task_id,
    )


@router.put(
    "/{task_id}",
    response_model=TaskOut,
)
def update_task(
    task_id: int,
    updated: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_task_service(
        db,
        current_user,
        task_id,
        updated,
    )


@router.patch(
    "/{task_id}/status",
    response_model=TaskOut,
)
def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_task_status_service(
        db,
        current_user,
        task_id,
        payload,
    )


@router.patch(
    "/{task_id}/assign",
    response_model=TaskOut,
)
def assign_task(
    task_id: int,
    assignment: TaskAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(MANAGEMENT_ROLES)
    ),
):
    return assign_task_service(
        db,
        current_user,
        task_id,
        assignment,
    )


@router.patch(
    "/{task_id}/smart-assign",
    response_model=TaskOut,
)
def smart_assign_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(MANAGEMENT_ROLES)
    ),
):
    return smart_assign_task_service(
        db,
        current_user,
        task_id,
    )


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            [
                "organization_admin",
            ]
        )
    ),
):
    return delete_task_service(
        db,
        current_user,
        task_id,
    )