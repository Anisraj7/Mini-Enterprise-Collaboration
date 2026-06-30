from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.meeting_attendee import (
    MeetingAttendeeCreate,
    MeetingAttendeeResponse,
)
from app.services.meeting_attendee_service import MeetingAttendeeService

router = APIRouter(
    prefix="/meetings/{meeting_id}/attendees",
    tags=["Meeting Attendees"],
)


@router.post(
    "",
    response_model=MeetingAttendeeResponse,
)
def add_attendee(
    meeting_id: int,
    payload: MeetingAttendeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MeetingAttendeeService.add_attendee(
        db=db,
        organization_id=current_user.organization_id,
        meeting_id=meeting_id,
        user_id=payload.user_id,
    )


@router.get(
    "",
    response_model=list[MeetingAttendeeResponse],
)
def list_attendees(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MeetingAttendeeService.list_attendees(
        db=db,
        organization_id=current_user.organization_id,
        meeting_id=meeting_id,
    )


@router.delete(
    "/{user_id}",
)
def remove_attendee(
    meeting_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    MeetingAttendeeService.remove_attendee(
        db=db,
        organization_id=current_user.organization_id,
        meeting_id=meeting_id,
        user_id=user_id,
    )

    return {"message": "Meeting attendee removed successfully"}
