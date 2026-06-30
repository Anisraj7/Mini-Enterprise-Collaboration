from sqlalchemy.orm import Session

from app.models.meeting_attendee import (
    MeetingAttendee
)


class MeetingAttendeeRepository:

    @staticmethod
    def create(
        db: Session,
        attendee: MeetingAttendee
    ) -> MeetingAttendee:
        db.add(attendee)
        db.commit()
        db.refresh(attendee)
        return attendee

    @staticmethod
    def get_by_id(
        db: Session,
        attendee_id: int
    ) -> MeetingAttendee | None:
        return (
            db.query(MeetingAttendee)
            .filter(
                MeetingAttendee.id == attendee_id
            )
            .first()
        )

    @staticmethod
    def get_attendees(
        db: Session,
        meeting_id: int
    ) -> list[MeetingAttendee]:
        return (
            db.query(MeetingAttendee)
            .filter(
                MeetingAttendee.meeting_id == meeting_id
            )
            .all()
        )

    @staticmethod
    def get_attendee(
        db: Session,
        meeting_id: int,
        user_id: int
    ) -> MeetingAttendee | None:
        return (
            db.query(MeetingAttendee)
            .filter(
                MeetingAttendee.meeting_id == meeting_id,
                MeetingAttendee.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        attendee: MeetingAttendee
    ) -> MeetingAttendee:
        db.commit()
        db.refresh(attendee)
        return attendee

    @staticmethod
    def delete(
        db: Session,
        attendee: MeetingAttendee
    ) -> None:
        db.delete(attendee)
        db.commit()
        
    @staticmethod
    def remove_attendee(
        db: Session,
        organization_id: int,
        meeting_id: int,
        user_id: int,
    ):
        attendee = (
            db.query(MeetingAttendee)
            .filter(
                MeetingAttendee.meeting_id == meeting_id,
                MeetingAttendee.user_id == user_id,
                MeetingAttendee.organization_id == organization_id,
            )
            .first()
        )

        if attendee:
            db.delete(attendee)
            db.commit()

        return attendee