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
            db.query(Notification)
            .filter(
                Notification.user_id
                == user.id
            )
        )

        if user.organization_id:

            query = query.filter(
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
            db.query(Notification)
            .filter(
                Notification.id
                == notification_id,
                Notification.user_id
                == user_id,
            )
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
            db.query(Notification)
            .filter(
                Notification.user_id
                == user_id,
                Notification.is_read
                == False,
            )
            .count()
        )