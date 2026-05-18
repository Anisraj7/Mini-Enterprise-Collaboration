from fastapi import (
    HTTPException,
    status,
)

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.core.cache import (
    cache_get,
    cache_set,
    invalidate_read_caches,
)

from app.models.user import User

from app.services.notification_service import (
    dispatch_kanban_update,
)

from app.services.task_service import (
    kanban_service,
    apply_task_status,
    
)


from app.repository.kanban_repository import (
    get_task_by_id,
    active_workspace_users_query,
    commit_refresh,
)


def update_task_status_service(
    task_id: int,
    new_status: str,
    user,
    db: Session,
):

    task = get_task_by_id(
        db,
        task_id,
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if (
        user.organization_id
        and task.organization_id != user.organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    apply_task_status(
        task,
        new_status,
        user,
        db,
    )

    commit_refresh(
        db,
        task,
    )

    invalidate_read_caches()

    users = active_workspace_users_query(
        db,
        user,
    )

    dispatch_kanban_update(
        [row[0] for row in users]
    )

    return task


def get_kanban_board_service(
    user,
    db: Session,
):

    cache_key = (
        f"kanban:board:"
        f"user:{user.id}:"
        f"role:{user.role}"
    )

    cached = cache_get(cache_key)

    if cached:
        return cached

    result = kanban_service(
        user,
        db,
    )

    result = jsonable_encoder(result)

    cache_set(
        cache_key,
        result,
    )

    return result