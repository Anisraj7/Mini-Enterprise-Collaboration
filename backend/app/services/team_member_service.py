from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.team_member import TeamMember

from app.repository.team_member_repository import (
    TeamMemberRepository,
)

from app.services.team_service import (
    TeamService,
)


class TeamMemberService:

    @staticmethod
    def add_member(
        db: Session,
        organization_id: int,
        team_id: int,
        user_id: int,
        role,
    ):

        TeamService.get_team(
            db,
            organization_id,
            team_id,
        )

        existing = TeamMemberRepository.get_member(
            db,
            team_id,
            user_id,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already in team",
            )

        member = TeamMember(
            organization_id=organization_id,
            team_id=team_id,
            user_id=user_id,
            role=role,
        )

        return TeamMemberRepository.create(
            db,
            member,
        )

    @staticmethod
    def list_members(
        db: Session,
        organization_id: int,
        team_id: int,
    ):

        TeamService.get_team(
            db,
            organization_id,
            team_id,
        )

        return TeamMemberRepository.get_team_members(
            db,
            team_id,
        )

    @staticmethod
    def remove_member(
        db: Session,
        organization_id: int,
        team_id: int,
        user_id: int,
    ):

        TeamService.get_team(
            db,
            organization_id,
            team_id,
        )

        member = TeamMemberRepository.get_member(
            db,
            team_id,
            user_id,
        )

        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team member not found",
            )

        return TeamMemberRepository.delete(
            db,
            member,
        )