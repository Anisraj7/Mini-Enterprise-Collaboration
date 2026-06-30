from fastapi import HTTPException

from app.models.meeting_note import (
    MeetingNote
)

from app.repository.meeting_note_repository import (
    MeetingNoteRepository
)

from app.services.meeting_service import (
    MeetingService
)


class MeetingNoteService:

    @staticmethod
    def create_note(
        db,
        organization_id,
        user_id,
        meeting_id,
        payload
    ):

        MeetingService.get_meeting(
            db,
            organization_id,
            meeting_id
        )

        note = MeetingNote(
            organization_id=organization_id,
            meeting_id=meeting_id,
            notes=payload.notes,
            created_by=user_id
        )

        return MeetingNoteRepository.create(
            db,
            note
        )

    @staticmethod
    def list_notes(
        db,
        organization_id,
        meeting_id
    ):

        MeetingService.get_meeting(
            db,
            organization_id,
            meeting_id
        )

        return (
            MeetingNoteRepository
            .get_meeting_notes(
                db,
                meeting_id
            )
        )

    @staticmethod
    def update_note(
        db,
        note_id,
        payload
    ):

        note = (
            MeetingNoteRepository.get_by_id(
                db,
                note_id
            )
        )

        if not note:
            raise HTTPException(
                status_code=404,
                detail="Note not found"
            )

        note.notes = payload.notes

        return MeetingNoteRepository.update(
            db,
            note
        )