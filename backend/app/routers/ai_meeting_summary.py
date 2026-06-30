from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.ai_meeting_summary import (
    AIMeetingSummaryCreate,
    AIMeetingSummaryResponse,
)

from app.services.ai_meeting_summary_service import (
    AIMeetingSummaryService,
)

router = APIRouter(
    tags=["AI Meeting Summary"]
)


@router.post(
    "/meetings/{meeting_id}/summary",
    response_model=AIMeetingSummaryResponse,
)
def create_summary(
    meeting_id: int,
    payload: AIMeetingSummaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AIMeetingSummaryService.create_summary(
        db=db,
        organization_id=current_user.organization_id,
        meeting_id=meeting_id,
        payload=payload,
    )


@router.get(
    "/meetings/{meeting_id}/summary",
    response_model=AIMeetingSummaryResponse,
)
def get_summary(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AIMeetingSummaryService.get_summary(
        db=db,
        organization_id=current_user.organization_id,
        meeting_id=meeting_id,
    )