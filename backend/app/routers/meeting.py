from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.meeting import (
    MeetingCreate,
    MeetingUpdate,
    MeetingResponse,
)

from app.services.meeting_service import (
    MeetingService,
)
from app.repository.meeting_repository import MeetingRepository

router = APIRouter(
    prefix="/meetings",
    tags=["Meetings"],
)


@router.post(
    "",
    response_model=MeetingResponse,
)
def create_meeting(
    payload: MeetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MeetingService.create_meeting(
        db=db,
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        payload=payload,
    )


@router.get(
    "",
    response_model=list[MeetingResponse],
)
def list_meetings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MeetingService.list_meetings(
        db=db,
        organization_id=current_user.organization_id,
    )


@router.get(
    "/{meeting_id}",
    response_model=MeetingResponse,
)
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Debug
    print("Current User:", current_user.id)
    print("Current Organization:", current_user.organization_id)

    meeting = MeetingRepository.get_by_id(
        db=db,
        meeting_id=meeting_id,
        organization_id=current_user.organization_id,
    )

    print("Meeting:", meeting)

    return MeetingService.get_meeting(
        db=db,
        organization_id=current_user.organization_id,
        meeting_id=meeting_id,
    )


@router.put(
    "/{meeting_id}",
    response_model=MeetingResponse,
)
def update_meeting(
    meeting_id: int,
    payload: MeetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MeetingService.update_meeting(
        db=db,
        organization_id=current_user.organization_id,
        meeting_id=meeting_id,
        payload=payload,
    )


@router.delete("/{meeting_id}")
def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    MeetingService.delete_meeting(
        db=db,
        organization_id=current_user.organization_id,
        meeting_id=meeting_id,
    )

    return {
        "message": "Meeting deleted successfully"
    }