from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.notification_preference import (
    NotificationPreference,
)

from app.repository.notification_preference_repository import (
    NotificationPreferenceRepository,
)

from app.schemas.notification_preference import (
    NotificationPreferenceUpdate,
)


class NotificationPreferenceService:

    @staticmethod
    def create_default_preferences(
        db: Session,
        user_id: int,
    ):

        existing = (
            NotificationPreferenceRepository.get_by_user_id(
                db,
                user_id,
            )
        )

        if existing:
            return existing

        preference = (
            NotificationPreference(
                user_id=user_id,
            )
        )

        return (
            NotificationPreferenceRepository.create(
                db,
                preference,
            )
        )

    @staticmethod
    def get_my_preferences(
        db: Session,
        user_id: int,
    ):
        preference = (
            NotificationPreferenceRepository.get_by_user_id(
                db,
                user_id,
            )
        )

        if not preference:
            preference = (
                NotificationPreferenceService.create_default_preferences(
                    db,
                    user_id,
                )
            )

        return preference

    @staticmethod
    def update_preferences(
        db: Session,
        user_id: int,
        payload: NotificationPreferenceUpdate,
    ):

        preference = (
            NotificationPreferenceRepository.get_by_user_id(
                db,
                user_id,
            )
        )

        if not preference:
            preference = (
                NotificationPreferenceService.create_default_preferences(
                    db,
                    user_id,
                )
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(
                preference,
                key,
                value,
            )

        return (
            NotificationPreferenceRepository.update(
                db,
                preference,
            )
        )
