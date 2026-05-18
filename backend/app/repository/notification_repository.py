from sqlalchemy.orm import Session

from app.models.notification import Notification


def notifications_query(
    db: Session,
    user,
):

    query = db.query(Notification).filter(
        Notification.user_id == user.id
    )

    if user.organization_id:
        query = query.filter(
            Notification.organization_id
            == user.organization_id
        )

    return query.order_by(
        Notification.created_at.desc()
    )


def get_notification_by_id(
    db: Session,
    notification_id: int,
    user_id: int,
):

    return (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id,
        )
        .first()
    )


def create_notification_repository(
    db: Session,
    notification: Notification,
):

    db.add(notification)

    db.flush()

    return notification


def commit_refresh(
    db: Session,
    model,
):

    db.commit()

    db.refresh(model)

    return model