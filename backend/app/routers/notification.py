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
    get_unread_count_service,
    mark_all_notifications_read_service,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


# =========================================
# GET USER NOTIFICATIONS
# =========================================
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


# =========================================
# GET UNREAD COUNT
# =========================================
@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_unread_count_service(
        db,
        user,
    )


# =========================================
# MARK SINGLE NOTIFICATION READ
# =========================================
@router.patch(
    "/{notification_id}/read"
)
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


# =========================================
# MARK ALL NOTIFICATIONS READ
# =========================================
@router.patch("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return mark_all_notifications_read_service(
        db,
        user,
    )