from fastapi import HTTPException, status

from app.repository.project_repository import (
    ProjectRepository,
)

from app.repository.meeting_repository import (
    MeetingRepository,
)

from app.repository.task_repository import (
    TaskRepository,
)


class CalendarService:

    @staticmethod
    def get_project_calendar(
        db,
        organization_id: int,
        project_id: int,
    ):

        project = ProjectRepository.get_by_id(
            db,
            project_id,
            organization_id,
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        meetings = MeetingRepository.get_by_project(
            db,
            organization_id,
            project_id,
        )

        tasks = TaskRepository.get_by_project(
            db,
            organization_id,
            project_id,
        )

        events = []

        for meeting in meetings:
            events.append(
                {
                    "id": meeting.id,
                    "type": "MEETING",
                    "title": meeting.title,
                    "start": meeting.start_time,
                    "end": meeting.end_time,
                    "status": meeting.status,
                }
            )

        for task in tasks:
            events.append(
                {
                    "id": task.id,
                    "type": "TASK",
                    "title": task.title,
                    "date": task.due_date,
                    "status": task.status,
                }
            )

        events.sort(
            key=lambda event: event.get("start") or event.get("date")
        )

        return {
            "project_id": project.id,
            "project_name": project.name,
            "events": events,
        }