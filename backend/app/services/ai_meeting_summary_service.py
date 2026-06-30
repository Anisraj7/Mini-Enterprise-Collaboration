from fastapi import HTTPException, status

from app.models.ai_meeting_summary import AIMeetingSummary

from app.repository.ai_meeting_summary_repository import (
    AIMeetingSummaryRepository,
)

from app.services.meeting_service import (
    MeetingService,
)


class AIMeetingSummaryService:

    @staticmethod
    def create_summary(
        db,
        organization_id,
        meeting_id,
        payload,
    ):

        MeetingService.get_meeting(
            db,
            organization_id,
            meeting_id,
        )

        existing = AIMeetingSummaryRepository.get_by_meeting(
            db,
            meeting_id,
        )

        if existing:
            existing.summary = payload.summary
            existing.action_items = payload.action_items
            existing.risks = payload.risks
            existing.decisions = payload.decisions

            return AIMeetingSummaryRepository.update(
                db,
                existing,
            )

        summary = AIMeetingSummary(
            organization_id=organization_id,
            meeting_id=meeting_id,
            summary=payload.summary,
            action_items=payload.action_items,
            risks=payload.risks,
            decisions=payload.decisions,
        )

        return AIMeetingSummaryRepository.create(
            db,
            summary,
        )

    @staticmethod
    def get_summary(
        db,
        organization_id,
        meeting_id,
    ):

        MeetingService.get_meeting(
            db,
            organization_id,
            meeting_id,
        )

        summary = AIMeetingSummaryRepository.get_by_meeting(
            db,
            meeting_id,
        )

        if not summary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meeting summary not found",
            )

        return summary