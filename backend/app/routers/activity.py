from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.core.permissions import require_roles

from app.db.database import get_db

from app.models.user import User

from app.schemas.activity import ActivityLogOut

from app.services.activity_service import (
    get_activity_logs_service,
)

router = APIRouter(
    prefix="/activity",
    tags=["Activity"],
)


@router.get(
    "/",
    response_model=Page[ActivityLogOut],
)
def get_activity_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            [
                "organization_admin",
                "workspace_admin",
                "manager",
            ]
        )
    ),
):
    return get_activity_logs_service(
        db,
        current_user,
    )