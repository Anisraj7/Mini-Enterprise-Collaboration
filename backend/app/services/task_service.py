from uuid import uuid4
import os
import shutil

from fastapi import HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.cache import cache_get, cache_set, invalidate_read_caches

from app.models.task import Task
from app.models.user import User

from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskAssign,
    TaskStatusUpdate,
)

from app.services.notification_service import (
    create_notification,
    dispatch_kanban_update,
)
from app.services.event_log_service import record_event
from app.services.sla_tracking_service import SLATrackingService


from app.repository.task_repository import (
    get_task_by_id,
    visible_tasks_query,
    assignable_users_query,
    create_task_repository,
    update_task_repository,
    delete_task_repository,
    commit_refresh,
)

from sqlalchemy import func, select


WORKFLOW_STATUSES = ("todo", "in_progress", "review", "done")

ALLOWED_TRANSITIONS = {
    "todo": ("in_progress",),
    "in_progress": ("review",),
    "review": ("done",),
    "done": (),
}


def normalize_status(value: str):

    status_value = getattr(value, "value", value)

    status_value = str(status_value).strip().lower()

    if status_value not in WORKFLOW_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported task status: {status_value}",
        )

    return status_value


def validate_status_transition(current_status: str, new_status: str):

    current = normalize_status(current_status)

    new = normalize_status(new_status)

    if current == new:
        return new

    if new not in ALLOWED_TRANSITIONS[current]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid transition: {current} -> {new}",
        )

    return new


def can_access_task(task: Task, user: User):

    if (
        user.organization_id and task.organization_id != user.organization_id):
        return False

    if user.role in (
        "super_admin",
        "organization_admin",
        "workspace_admin",
    ):
        return True

    if user.role == "manager":
        return (
            task.created_by_id == user.id
            or task.assigned_to_id == user.id
        )

    return task.assigned_to_id == user.id

def get_task_or_404(db: Session, task_id: int):

    task = get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


def ensure_user_exists(db: Session, user_id: int):

    user = db.execute(
        select(User).where(User.id == user_id)
    ).scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found",
        )

    return user


def workspace_user_ids(db: Session, user: User):

    query = select(User.id).where(
        User.is_active.is_(True)
    )

    if user.organization_id:
        query = query.where(
            User.organization_id == user.organization_id
        )

    return [row[0] for row in db.execute(query).all()]


def apply_task_status(task: Task, new_status: str, user: User, db: Session):

    status_value = validate_status_transition(
        task.status,
        new_status,
    )

    if not can_access_task(task, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    if task.status != status_value:

        task.status = status_value

        task.updated_by = user.id

        record_event(
            db,
            user_id=user.id,
            action="TASK_STATUS_UPDATED",
            entity_type="TASK",
            entity_id=task.id,
            organization_id=user.organization_id,
        )

    return task


def create_task_service(
    db: Session,
    current_user: User,
    task: TaskCreate,
):

    if task.assigned_to_id:

        assigned_user = ensure_user_exists(
            db,
            task.assigned_to_id,
        )

        if (
            current_user.organization_id
            and assigned_user.organization_id != current_user.organization_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot assign outside organization",
            )

    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority.value,
        due_date=task.due_date,
        created_by_id=current_user.id,
        assigned_to_id=task.assigned_to_id,
        updated_by=current_user.id,
        organization_id=current_user.organization_id,
    )

    create_task_repository(db, new_task)

    try:
        SLATrackingService.start_sla_tracking(
            db,
            "Task",
            new_task.id,
            new_task.priority,
        )
        db.refresh(new_task)

    except HTTPException as e:
        print("SLA ERROR:", e.detail)

    record_event(
        db,
        user_id=current_user.id,
        action="TASK_CREATED",
        entity_type="TASK",
        entity_id=new_task.id,
        organization_id=current_user.organization_id,
    )

    if new_task.assigned_to_id:
        create_notification(
            db,
            new_task.assigned_to_id,
            f"Task assigned: {new_task.title}",
            current_user.organization_id,
        )

    commit_refresh(db, new_task)

    invalidate_read_caches()

    dispatch_kanban_update(
        workspace_user_ids(db, current_user)
    )

    return new_task


def create_task_with_document_service(
    db: Session,
    current_user: User,
    title: str,
    description: str,
    status_value: str,
    priority: str,
    due_date: str,
    assigned_to_id: int,
    document: UploadFile,
):

    file_path = None

    if assigned_to_id:

        assigned_user = ensure_user_exists(
            db,
            assigned_to_id,
        )

        if (
            current_user.organization_id
            and assigned_user.organization_id != current_user.organization_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot assign outside organization",
            )

    if document:

        os.makedirs("uploads", exist_ok=True)

        filename = f"{uuid4()}_{document.filename}"

        file_path = os.path.join(
            "uploads",
            filename,
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(document.file, buffer)

    new_task = Task(
        title=title,
        description=description,
        status=status_value,
        priority=priority,
        due_date=due_date,
        created_by_id=current_user.id,
        assigned_to_id=assigned_to_id,
        updated_by=current_user.id,
        document=file_path,
        organization_id=current_user.organization_id,
    )

    create_task_repository(db, new_task)

    try:
        SLATrackingService.start_sla_tracking(
            db,
            "Task",
            new_task.id,
            new_task.priority,
        )
        db.refresh(new_task)

    except HTTPException as e:
        print("SLA ERROR:", e.detail)

    commit_refresh(db, new_task)

    invalidate_read_caches()

    dispatch_kanban_update(
        workspace_user_ids(db, current_user)
    )

    return new_task


def list_tasks_service(
    db: Session,
    current_user: User,
):

    query = visible_tasks_query(
        db,
        current_user,
    )

    query = query.order_by(
        Task.created_at.desc()
    )

    return paginate(db, query)


def get_task_service(
    db: Session,
    current_user: User,
    task_id: int,
):

    cache_key = f"task:{task_id}"

    cached = cache_get(cache_key)

    if cached:
        return cached

    task = get_task_or_404(db, task_id)

    if not can_access_task(task, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    result = jsonable_encoder(task)

    cache_set(cache_key, result)

    return result


def kanban_service(
    db: Session,
    current_user: User,
):

    cache_key = f"kanban:{current_user.id}"

    cached = cache_get(cache_key)

    if cached:
        return cached

    board = {
        status_name: []
        for status_name in WORKFLOW_STATUSES
    }

    tasks = db.execute(
        visible_tasks_query(db, current_user)
        .order_by(Task.updated_at.desc())
    ).scalars().all()

    for task in tasks:

        board.setdefault(task.status, []).append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
                "created_by_id": task.created_by_id,
                "assigned_to_id": task.assigned_to_id,
                "assigned_to_name": task.assigned_to_name,
                "updated_by": task.updated_by,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "sla_status": task.sla_status,
                "sla_due_time": task.sla_due_time,
                "is_sla_breached": task.is_sla_breached,
            }
        )

    cache_set(cache_key, board)

    return board


def recommendation_service(
    db: Session,
    current_user: User,
):

    candidates = db.execute(assignable_users_query(
        db,
        current_user,
    )).scalars().all()

    if not candidates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No assignable users found",
        )

    open_counts = dict(
        db.execute(select(
            Task.assigned_to_id,
            func.count(Task.id),
        )
        .where(
            Task.status != "done",
            Task.assigned_to_id.isnot(None),
        )
        .group_by(Task.assigned_to_id)
        ).all()
    )

    done_counts = dict(
        db.execute(select(
            Task.assigned_to_id,
            func.count(Task.id),
        )
        .where(
            Task.status == "done",
            Task.assigned_to_id.isnot(None),
        )
        .group_by(Task.assigned_to_id)
        ).all()
    )

    def score(candidate):

        workload = open_counts.get(candidate.id, 0)

        completed = done_counts.get(candidate.id, 0)

        return (
            workload,
            -completed,
            candidate.name.lower(),
        )

    selected = min(candidates, key=score)

    return {
        "id": selected.id,
        "name": selected.name,
        "email": selected.email,
        "role": selected.role,
        "active_tasks": open_counts.get(selected.id, 0),
        "completed_tasks": done_counts.get(selected.id, 0),
    }


def update_task_service(
    db: Session,
    current_user: User,
    task_id: int,
    updated: TaskUpdate,
):

    task = get_task_or_404(db, task_id)

    if not can_access_task(task, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    changes = updated.model_dump(exclude_unset=True)

    if "status" in changes:
        apply_task_status(
            task,
            changes.pop("status"),
            current_user,
            db,
        )

    for key, value in changes.items():

        if hasattr(value, "value"):
            value = value.value

        setattr(task, key, value)

    task.updated_by = current_user.id

    update_task_repository(db, task)

    commit_refresh(db, task)

    invalidate_read_caches()

    dispatch_kanban_update(
        workspace_user_ids(db, current_user)
    )

    return task


def update_task_status_service(
    db: Session,
    current_user: User,
    task_id: int,
    payload: TaskStatusUpdate,
):

    task = get_task_or_404(db, task_id)

    apply_task_status(
        task,
        payload.status,
        current_user,
        db,
    )

    update_task_repository(db, task)

    if task.status == "done":
        try:
            tracking = SLATrackingService.get_sla_record(db, "Task", task.id)
            if tracking and not tracking.completed_time:
                SLATrackingService.complete_sla(db, tracking.id)
                db.refresh(task)
        except HTTPException:
            pass

    commit_refresh(db, task)

    invalidate_read_caches()

    return task


def assign_task_service(
    db: Session,
    current_user: User,
    task_id: int,
    assignment: TaskAssign,
):

    task = get_task_or_404(db, task_id)

    assigned_user = ensure_user_exists(
        db,
        assignment.assigned_to_id,
    )

    if (
        current_user.organization_id
        and assigned_user.organization_id != current_user.organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot assign outside organization",
        )

    task.assigned_to_id = assignment.assigned_to_id

    task.updated_by = current_user.id

    update_task_repository(db, task)

    create_notification(
        db,
        assignment.assigned_to_id,
        f"Task assigned: {task.title}",
        current_user.organization_id,
    )

    commit_refresh(db, task)

    invalidate_read_caches()

    return task


def smart_assign_task_service(
    db: Session,
    current_user: User,
    task_id: int,
):

    task = get_task_or_404(db, task_id)

    recommendation = recommendation_service(
        db,
        current_user,
    )

    task.assigned_to_id = recommendation["id"]

    task.updated_by = current_user.id

    update_task_repository(db, task)

    commit_refresh(db, task)

    invalidate_read_caches()

    return task


def delete_task_service(
    db: Session,
    current_user: User,
    task_id: int,
):

    task = get_task_or_404(db, task_id)

    delete_task_repository(db, task)

    db.commit()

    invalidate_read_caches()

    return {
        "message": "Task deleted"
    }
