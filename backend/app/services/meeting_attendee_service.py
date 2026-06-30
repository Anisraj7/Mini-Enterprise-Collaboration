from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.meeting_attendee import (
    MeetingAttendee
)

from app.repository.meeting_attendee_repository import (
    MeetingAttendeeRepository
)

from app.services.meeting_service import (
    MeetingService
)


class MeetingAttendeeService:

    @staticmethod
    def add_attendee(
        db: Session,
        organization_id: int,
        meeting_id: int,
        user_id: int
    ):

        MeetingService.get_meeting(
            db,
            organization_id,
            meeting_id
        )

        existing = (
            MeetingAttendeeRepository.get_attendee(
                db,
                meeting_id,
                user_id
            )
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already invited"
            )

        attendee = MeetingAttendee(
            organization_id=organization_id,
            meeting_id=meeting_id,
            user_id=user_id
        )

        return MeetingAttendeeRepository.create(
            db,
            attendee
        )

    @staticmethod
    def list_attendees(
        db: Session,
        organization_id: int,
        meeting_id: int
    ):

        MeetingService.get_meeting(
            db,
            organization_id,
            meeting_id
        )

        return (
            MeetingAttendeeRepository
            .get_attendees(
                db,
                meeting_id
            )
        )
        
    @staticmethod
    def remove_attendee(
        db: Session,
        organization_id: int,
        meeting_id: int,
        user_id: int,
    ):
        return MeetingAttendeeRepository.remove_attendee(
            db,
            organization_id,
            meeting_id,
            user_id,
        )