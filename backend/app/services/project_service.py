from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project import Project
from app.repository.project_repository import (
    ProjectRepository
)


class ProjectService:

    @staticmethod
    def create_project(
        db: Session,
        organization_id: int,
        payload,
    ):

        project = Project(
            organization_id=organization_id,
            workspace_id=payload.workspace_id,
            owner_id=payload.owner_id,
            name=payload.name,
            description=payload.description,
            priority=payload.priority,
            start_date=payload.start_date,
            end_date=payload.end_date
        )

        return ProjectRepository.create(
            db,
            project
        )

    @staticmethod
    def get_project(
        db: Session,
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

        return project

    @staticmethod
    def list_projects(
        db: Session,
        organization_id: int
    ):
        return ProjectRepository.get_all(
            db,
            organization_id
        )
        
    @staticmethod
    def update_project(
        db: Session,
        organization_id: int,
        project_id: int,
        payload,
    ):
        project = ProjectService.get_project(
            db,
            organization_id,
            project_id,
        )

        for key, value in payload.model_dump(
            exclude_unset=True
        ).items():
            setattr(project, key, value)

        return ProjectRepository.update(
            db,
            project,
        )


    @staticmethod
    def delete_project(
        db: Session,
        organization_id: int,
        project_id: int,
    ):
        project = ProjectService.get_project(
            db,
            organization_id,
            project_id,
        )

        return ProjectRepository.delete(
            db,
            project,
        )
