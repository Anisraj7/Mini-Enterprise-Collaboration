from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.core.dependencies import (
    get_current_user,
)

from app.db.database import get_db

from app.schemas.notification import (
    NotificationOut,
)

from app.services.notification_service import (
    get_notifications_service,
    mark_notification_read_service,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get(
    "/",
    response_model=Page[NotificationOut],
)
def get_notifications(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_notifications_service(
        db,
        user,
    )


@router.patch("/{notification_id}/read")
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return mark_notification_read_service(
        notification_id,
        db,
        user,
    )