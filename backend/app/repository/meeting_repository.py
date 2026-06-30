from sqlalchemy.orm import Session

from app.models.meeting import Meeting


class MeetingRepository:

    @staticmethod
    def create(
        db: Session,
        meeting: Meeting
    ) -> Meeting:
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        return meeting

    @staticmethod
    def get_by_id(
        db: Session,
        meeting_id: int,
        organization_id: int
    ) -> Meeting | None:
        return (
            db.query(Meeting)
            .filter(
                Meeting.id == meeting_id,
                Meeting.organization_id == organization_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        organization_id: int
    ) -> list[Meeting]:
        return (
            db.query(Meeting)
            .filter(
                Meeting.organization_id == organization_id
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        meeting: Meeting
    ) -> Meeting:
        db.commit()
        db.refresh(meeting)
        return meeting
    
    @staticmethod
    def get_by_project(
        db: Session,
        organization_id: int,
        project_id: int
    ) -> list[Meeting]:
        return (
            db.query(Meeting)
            .filter(
                Meeting.organization_id == organization_id,
                Meeting.project_id == project_id,
                Meeting.status != "CANCELLED"
            )
            .all()
        )
        
    @staticmethod
    def delete(
        db: Session,
        meeting: Meeting,
    ):
        db.delete(meeting)
        db.commit()