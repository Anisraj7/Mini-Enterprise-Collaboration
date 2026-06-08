from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.cache import (
    cache_get,
    cache_set,
    invalidate_read_caches,
)

from app.models.comments import Comment

from app.services.notification_service import (
    create_notification,
)
from app.services.event_log_service import record_event

from app.services.task_service import (
    can_access_task,
)

from app.repository.comment_repository import (
    get_task_by_id,
    comments_query,
    create_comment_repository,
    commit_refresh,
)


def create_comment_service(
    task_id: int,
    data,
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

    if not can_access_task(task, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    if (
        data.is_internal
        and user.role == "employee"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employees cannot add internal comments",
        )

    comment = Comment(
        task_id=task_id,
        user_id=user.id,
        content=data.content,
        is_internal=bool(data.is_internal),
        organization_id=user.organization_id,
    )

    create_comment_repository(
        db,
        comment,
    )

    record_event(
        db,
        user_id=user.id,
        action="COMMENT_ADDED",
        entity_type="COMMENT",
        entity_id=comment.id,
        organization_id=user.organization_id,
    )

    for recipient_id in {
        task.created_by_id,
        task.assigned_to_id,
    } - {
        None,
        user.id,
    }:
        create_notification(
            db,
            recipient_id,
            f"New comment on task: {task.title}",
            user.organization_id,
        )

    commit_refresh(
        db,
        comment,
    )

    invalidate_read_caches()

    return comment


def get_comments_service(
    task_id: int,
    user,
    db: Session,
):

    cache_key = (
        f"comments:list:"
        f"user:{user.id}:"
        f"role:{user.role}:"
        f"task:{task_id}"
    )

    cached = cache_get(cache_key)

    if cached:
        return cached

    task = get_task_by_id(
        db,
        task_id,
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if not can_access_task(task, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    query = comments_query(
        db,
        task_id,
        user,
    )

    result = paginate(db, query)

    result = jsonable_encoder(result)

    cache_set(
        cache_key,
        result,
    )

    return result
