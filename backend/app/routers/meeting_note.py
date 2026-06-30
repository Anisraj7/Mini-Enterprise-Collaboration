from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.meeting_note import (
    MeetingNoteCreate,
    MeetingNoteUpdate,
    MeetingNoteResponse,
)

from app.services.meeting_note_service import (
    MeetingNoteService,
)

router = APIRouter(
    tags=["Meeting Notes"]
)


@router.post(
    "/meetings/{meeting_id}/notes",
    response_model=MeetingNoteResponse,
)
def create_note(
    meeting_id: int,
    payload: MeetingNoteCreate,
    db: Session = Depends(get_db),
):
    return MeetingNoteService.create_note(
        db=db,
        organization_id=4,
        user_id=5,
        meeting_id=meeting_id,
        payload=payload,
    )


@router.get(
    "/meetings/{meeting_id}/notes",
    response_model=list[MeetingNoteResponse],
)
def list_notes(
    meeting_id: int,
    db: Session = Depends(get_db),
):
    return MeetingNoteService.list_notes(
        db=db,
        organization_id=4,
        meeting_id=meeting_id,
    )


@router.put(
    "/meeting-notes/{note_id}",
    response_model=MeetingNoteResponse,
)
def update_note(
    note_id: int,
    payload: MeetingNoteUpdate,
    db: Session = Depends(get_db),
):
    return MeetingNoteService.update_note(
        db=db,
        note_id=note_id,
        payload=payload,
    )