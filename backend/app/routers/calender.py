from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

from app.services.calender_service import (
    CalendarService,
)

router = APIRouter(
    tags=["Calendar"],
)


@router.get(
    "/projects/{project_id}/calendar",
)
def get_calendar(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CalendarService.get_project_calendar(
        db=db,
        organization_id=current_user.organization_id,
        project_id=project_id,
    )