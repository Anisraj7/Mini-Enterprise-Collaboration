import asyncio

from fastapi import (
    HTTPException,
    status,
)

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.cache import (
    cache_get,
    cache_set,
    invalidate_read_caches,
)

from app.models.notification import Notification

from app.services.websocket_manager import (
    manager,
)

from app.repository.notification_repository import (
    notifications_query,
    get_notification_by_id,
    create_notification_repository,
    commit_refresh,
)


def _dispatch_ws_message(
    user_id: int,
    payload,
):

    loop = manager.loop

    if not loop:
        return

    asyncio.run_coroutine_threadsafe(
        manager.send_message(
            user_id,
            payload,
        ),
        loop,
    )


def dispatch_kanban_update(
    user_ids,
):

    loop = manager.loop

    if not loop:
        return

    asyncio.run_coroutine_threadsafe(
        manager.broadcast_to_users(
            user_ids,
            {
                "type": "kanban_updated",
                "message": "Kanban board updated",
            },
        ),
        loop,
    )


def create_notification(
    db: Session,
    user_id: int,
    message: str,
    organization_id: int | None = None,
):

    notification = Notification(
        user_id=user_id,
        message=message,
        organization_id=organization_id,
    )

    create_notification_repository(
        db,
        notification,
    )

    invalidate_read_caches()

    _dispatch_ws_message(
        user_id,
        {
            "type": "notification",
            "message": message,
            "notification": {
                "user_id": user_id,
                "message": message,
                "organization_id": organization_id,
            },
        },
    )

    return notification


async def push_notification(
    user_id: int,
    message: str,
):

    await manager.send_message(
        user_id,
        message,
    )


def get_notifications_service(
    db: Session,
    user,
):

    cache_key = (
        f"notifications:list:"
        f"user:{user.id}"
    )

    cached = cache_get(cache_key)

    if cached:
        return cached

    query = notifications_query(
        db,
        user,
    )

    result = paginate(query)

    result = jsonable_encoder(result)

    cache_set(
        cache_key,
        result,
    )

    return result


def mark_notification_read_service(
    notification_id: int,
    db: Session,
    user,
):

    notification = get_notification_by_id(
        db,
        notification_id,
        user.id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    notification.is_read = True

    commit_refresh(
        db,
        notification,
    )

    invalidate_read_caches()

    return {
        "message": "Notification updated"
    }