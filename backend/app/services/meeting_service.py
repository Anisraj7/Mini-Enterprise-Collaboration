from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.meeting import Meeting

from app.repository.meeting_repository import (
    MeetingRepository,
)

from app.services.project_service import (
    ProjectService,
)

from app.schemas.meeting import (
    MeetingUpdate,
)


class MeetingService:

    @staticmethod
    def create_meeting(
        db: Session,
        organization_id: int,
        user_id: int,
        payload,
    ):

        ProjectService.get_project(
            db,
            organization_id,
            payload.project_id,
        )

        if payload.start_time >= payload.end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be after start time",
            )

        meeting = Meeting(
            organization_id=organization_id,
            project_id=payload.project_id,
            title=payload.title,
            description=payload.description,
            start_time=payload.start_time,
            end_time=payload.end_time,
            created_by=user_id,
        )

        return MeetingRepository.create(
            db,
            meeting,
        )

    @staticmethod
    def get_meeting(
        db: Session,
        organization_id: int,
        meeting_id: int,
    ):

        meeting = MeetingRepository.get_by_id(
            db,
            meeting_id,
            organization_id,
        )

        if not meeting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meeting not found",
            )

        return meeting

    @staticmethod
    def list_meetings(
        db: Session,
        organization_id: int,
    ):
        return MeetingRepository.get_all(
            db,
            organization_id,
        )

    @staticmethod
    def update_meeting(
        db: Session,
        organization_id: int,
        meeting_id: int,
        payload: MeetingUpdate,
    ):

        meeting = MeetingService.get_meeting(
            db,
            organization_id,
            meeting_id,
        )

        if (
            payload.start_time is not None
            and payload.end_time is not None
            and payload.start_time >= payload.end_time
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be after start time",
            )

        for key, value in payload.model_dump(
            exclude_unset=True,
        ).items():
            setattr(meeting, key, value)

        return MeetingRepository.update(
            db,
            meeting,
        )

    @staticmethod
    def delete_meeting(
        db: Session,
        organization_id: int,
        meeting_id: int,
    ):

        meeting = MeetingService.get_meeting(
            db,
            organization_id,
            meeting_id,
        )

        return MeetingRepository.delete(
            db,
            meeting,
        )