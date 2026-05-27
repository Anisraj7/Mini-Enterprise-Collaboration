from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user

from app.schemas.notification_preference import (
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate,
)

from app.services.notification_preference_service import (
    NotificationPreferenceService,
)

router = APIRouter(
    prefix="/notification-preferences",
    tags=["Notification Preferences"],
)


@router.post(
    "/default/{user_id}",
    response_model=NotificationPreferenceResponse,
)
def create_default_preferences(
    user_id: int,
    db: Session = Depends(get_db),
):
    return (
        NotificationPreferenceService.create_default_preferences(
            db,
            user_id,
        )
    )


@router.get(
    "/me",
    response_model=NotificationPreferenceResponse,
)
def get_my_preferences(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return (
        NotificationPreferenceService.get_my_preferences(
            db,
            user.id,
        )
    )


@router.put(
    "/me",
    response_model=NotificationPreferenceResponse,
)
def update_preferences(
    payload: NotificationPreferenceUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return (
        NotificationPreferenceService.update_preferences(
            db,
            user.id,
            payload,
        )
    )
