from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.notification import (
    Notification,
)


class NotificationRepository:

    @staticmethod
    def notifications_query(
        db: Session,
        user,
    ):

        query = (
            select(Notification)
            .where(
                Notification.user_id
                == user.id
            )
        )

        if user.organization_id:

            query = query.where(
                Notification.organization_id
                == user.organization_id
            )

        return query.order_by(
            Notification.created_at.desc()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        notification_id: int,
        user_id: int,
    ):

        return (
            db.execute(select(Notification).where(
                Notification.id
                == notification_id,
                Notification.user_id
                == user_id,
            ))
            .scalars()
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        notification: Notification,
    ):

        db.add(notification)

        db.flush()

        return notification

    @staticmethod
    def commit_refresh(
        db: Session,
        model,
    ):

        db.commit()

        db.refresh(model)

        return model

    @staticmethod
    def unread_count(
        db: Session,
        user_id: int,
    ):

        return (
            db.execute(select(func.count(Notification.id)).where(
                Notification.user_id
                == user_id,
                Notification.is_read.is_(False),
            ))
            .scalar_one()
        )
