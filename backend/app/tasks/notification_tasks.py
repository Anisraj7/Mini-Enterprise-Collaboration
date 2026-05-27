from app.core.celery_app import (
    celery_app,
)

from app.db.database import SessionLocal

from app.schemas.notification import (
    NotificationCreate,
)

from app.services.notification_service import (
    NotificationService,
)


@celery_app.task(
    name="app.tasks.notification_tasks.send_notification_task"
)
def send_notification_task(
    user_id: int,
    title: str,
    message: str,
    notification_type: str,
    priority: str = "MEDIUM",
):

    db = SessionLocal()

    try:

        payload = NotificationCreate(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
        )

        NotificationService.create_notification(
            db,
            payload,
        )

        print(
            f"Notification sent to user {user_id}"
        )

    finally:
        db.close()