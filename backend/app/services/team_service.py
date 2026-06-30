from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.team import Team
from app.repository.team_repository import TeamRepository
from app.schemas.team import TeamCreate, TeamUpdate


class TeamService:

    @staticmethod
    def create_team(
        db: Session,
        organization_id: int,
        user_id: int,
        payload: TeamCreate
    ) -> Team:

        team = Team(
            organization_id=organization_id,
            workspace_id=payload.workspace_id,
            name=payload.name,
            description=payload.description,
            created_by=user_id
        )

        return TeamRepository.create(db, team)

    @staticmethod
    def get_team(
        db: Session,
        organization_id: int,
        team_id: int
    ) -> Team:

        team = TeamRepository.get_by_id(
            db,
            team_id,
            organization_id
        )

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )

        return team

    @staticmethod
    def list_teams(
        db: Session,
        organization_id: int
    ):
        return TeamRepository.get_all(
            db,
            organization_id
        )

    @staticmethod
    def update_team(
        db: Session,
        organization_id: int,
        team_id: int,
        payload: TeamUpdate
    ):

        team = TeamService.get_team(
            db,
            organization_id,
            team_id
        )

        for key, value in payload.model_dump(
            exclude_unset=True
        ).items():
            setattr(team, key, value)

        return TeamRepository.update(db, team)

    @staticmethod
    def delete_team(
        db: Session,
        organization_id: int,
        team_id: int
    ):

        team = TeamService.get_team(
            db,
            organization_id,
            team_id
        )

        return TeamRepository.delete(
            db,
            team
        )