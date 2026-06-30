from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project_team import ProjectTeam
from app.repository.project_team_repository import (
    ProjectTeamRepository
)

from app.services.project_service import (
    ProjectService
)

from app.services.team_service import (
    TeamService
)


class ProjectTeamService:

    @staticmethod
    def assign_team(
        db: Session,
        organization_id: int,
        project_id: int,
        team_id: int
    ):

        ProjectService.get_project(
            db,
            organization_id,
            project_id
        )

        TeamService.get_team(
            db,
            organization_id,
            team_id
        )

        existing = (
            ProjectTeamRepository.get_mapping(
                db,
                project_id,
                team_id
            )
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team already assigned"
            )

        mapping = ProjectTeam(
            organization_id=organization_id,
            project_id=project_id,
            team_id=team_id
        )

        return ProjectTeamRepository.create(
            db,
            mapping
        )
        
    @staticmethod
    def list_project_teams(
        db: Session,
        organization_id: int,
        project_id: int
    ):
        ProjectService.get_project(
            db,
            organization_id,
            project_id
        )

        return ProjectTeamRepository.get_project_teams(
            db,
            project_id
        )

    @staticmethod
    def remove_team(
        db: Session,
        organization_id: int,
        project_id: int,
        team_id: int,
    ):
        ProjectService.get_project(
            db,
            organization_id,
            project_id,
        )

        TeamService.get_team(
            db,
            organization_id,
            team_id,
        )

        mapping = ProjectTeamRepository.get_mapping(
            db,
            project_id,
            team_id,
        )

        if not mapping:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project team assignment not found",
            )

        ProjectTeamRepository.delete(
            db,
            mapping,
        )

        return mapping
