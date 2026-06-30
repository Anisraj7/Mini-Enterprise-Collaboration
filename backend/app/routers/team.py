from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.team import (
    TeamCreate,
    TeamUpdate,
    TeamResponse
)
from app.services.team_service import TeamService

from app.core.permissions import require_roles
from app.models.enums import UserRole

read_roles = [
    UserRole.ORGANIZATION_ADMIN.value,
    UserRole.WORKSPACE_ADMIN.value,
    UserRole.MANAGER.value,
    UserRole.EMPLOYEE.value,
]

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("", response_model=TeamResponse)
def create_team(
    payload: TeamCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(read_roles)),
):
    return TeamService.create_team(
        db=db,
        organization_id=current_user.organization_id,      # from auth later
        user_id=current_user.id,        # from auth later
        payload=payload
    )


@router.get("", response_model=list[TeamResponse])
def list_teams(
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(read_roles)),
):
    return TeamService.list_teams(
        db,
        current_user.organization_id,
    )


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(read_roles)),
):
    return TeamService.get_team(
        db,
        current_user.organization_id,
        team_id=team_id
    )


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    payload: TeamUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(read_roles)),
):
    return TeamService.update_team(
        db,
        current_user.organization_id,
        team_id=team_id,
        payload=payload
    )


@router.delete("/{team_id}")
def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(read_roles)),
):
    TeamService.delete_team(
        db,
        current_user.organization_id,
        team_id=team_id
    )

    return {"message": "Team archived"}