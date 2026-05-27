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
from app.models.notification_preference import NotificationPreference

from app.services.websocket_manager import (
    manager,
)

from app.repository.notification_repository import (
    NotificationRepository
)


# =========================================
# WEBSOCKET DISPATCH
# =========================================
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


# =========================================
# KANBAN UPDATE DISPATCH
# =========================================
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


# =========================================
# CREATE NOTIFICATION
# =========================================
def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str | int | None = None,
    notification_type: str = "GENERAL",
    priority: str = "MEDIUM",
    organization_id: int | None = None,
):
    if isinstance(message, int) and organization_id is None:
        organization_id = message
        message = title
        notification_type = "GENERAL"

    if message is None:
        message = title

    preference = (
        db.query(NotificationPreference)
        .filter(NotificationPreference.user_id == user_id)
        .first()
    )

    if preference and not preference.in_app_enabled:
        return None

    preference_field_by_type = {
        "TASK": "task_notifications",
        "APPROVAL": "approval_notifications",
        "ESCALATION": "escalation_notifications",
        "DOCUMENT": "document_notifications",
    }
    preference_field = preference_field_by_type.get(str(notification_type).upper())

    if preference and preference_field and not getattr(preference, preference_field):
        return None

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        priority=priority,
        organization_id=organization_id,
    )

    NotificationRepository.create(
        db,
        notification,
    )

    NotificationRepository.commit_refresh(
        db,
        notification,
    )

    invalidate_read_caches()

    _dispatch_ws_message(
        user_id,
        {
            "type": "notification",
            "title": title,
            "message": message,
            "notification_type": notification_type,
            "priority": priority,
            "notification": {
                "id": notification.id,
                "user_id": user_id,
                "title": title,
                "message": message,
                "notification_type": notification_type,
                "priority": priority,
                "organization_id": organization_id,
                "is_read": False,
                "created_at": str(
                    notification.created_at
                ),
            },
        },
    )

    return notification


# =========================================
# PUSH LIVE NOTIFICATION
# =========================================
async def push_notification(
    user_id: int,
    payload,
):

    await manager.send_message(
        user_id,
        payload,
    )


# =========================================
# GET USER NOTIFICATIONS
# =========================================
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

    query = NotificationRepository.notifications_query(
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


# =========================================
# GET UNREAD COUNT
# =========================================
def get_unread_count_service(
    db: Session,
    user,
):

    cache_key = (
        f"notifications:unread:"
        f"user:{user.id}"
    )

    cached = cache_get(cache_key)

    if cached is not None:
        return {
            "unread_count": cached
        }

    count = (
        db.query(Notification)
        .filter(
            Notification.user_id
            == user.id,
            Notification.is_read
            == False,
        )
        .count()
    )

    cache_set(
        cache_key,
        count,
    )

    return {
        "unread_count": count
    }


# =========================================
# MARK NOTIFICATION READ
# =========================================
def mark_notification_read_service(
    notification_id: int,
    db: Session,
    user,
):

    notification = NotificationRepository.get_by_id(
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

    NotificationRepository.commit_refresh(
        db,
        notification,
    )

    invalidate_read_caches()

    return {
        "message": "Notification updated"
    }


# =========================================
# MARK ALL NOTIFICATIONS READ
# =========================================
def mark_all_notifications_read_service(
    db: Session,
    user,
):

    notifications = (
        NotificationRepository.notifications_query(
            db,
            user,
        )
        .filter(
            Notification.is_read == False
        )
        .all()
    )

    for notification in notifications:
        notification.is_read = True

    db.commit()

    invalidate_read_caches()

    return {
        "message": "All notifications marked as read"
    }


class NotificationService:
    @staticmethod
    def create_notification(db: Session, payload):
        return create_notification(
            db=db,
            user_id=payload.user_id,
            title=payload.title,
            message=payload.message,
            notification_type=payload.notification_type,
            priority=payload.priority,
            organization_id=getattr(payload, "organization_id", None),
        )
