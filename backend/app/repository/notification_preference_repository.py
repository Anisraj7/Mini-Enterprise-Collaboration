from sqlalchemy.orm import Session

from app.models.notification_preference import (
    NotificationPreference,
)


class NotificationPreferenceRepository:

    @staticmethod
    def create(
        db: Session,
        preference: NotificationPreference,
    ):
        db.add(preference)

        db.commit()

        db.refresh(preference)

        return preference

    @staticmethod
    def update(
        db: Session,
        preference: NotificationPreference,
    ):
        db.commit()

        db.refresh(preference)

        return preference

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(NotificationPreference)
            .filter(
                NotificationPreference.user_id
                == user_id
            )
            .first()
        )