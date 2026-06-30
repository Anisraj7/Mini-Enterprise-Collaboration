from sqlalchemy.orm import Session

from app.models.ai_meeting_summary import (
    AIMeetingSummary
)


class AIMeetingSummaryRepository:

    @staticmethod
    def create(
        db: Session,
        summary: AIMeetingSummary
    ) -> AIMeetingSummary:
        db.add(summary)
        db.commit()
        db.refresh(summary)
        return summary

    @staticmethod
    def get_by_meeting(
        db: Session,
        meeting_id: int
    ) -> AIMeetingSummary | None:
        return (
            db.query(AIMeetingSummary)
            .filter(
                AIMeetingSummary.meeting_id == meeting_id
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        summary: AIMeetingSummary
    ) -> AIMeetingSummary:
        db.commit()
        db.refresh(summary)
        return summary

    @staticmethod
    def delete(
        db: Session,
        summary: AIMeetingSummary
    ) -> None:
        db.delete(summary)
        db.commit()