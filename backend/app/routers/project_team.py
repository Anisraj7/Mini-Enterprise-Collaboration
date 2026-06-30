from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

from app.schemas.project_team import (
    ProjectTeamCreate,
    ProjectTeamResponse,
)

from app.services.project_team_service import (
    ProjectTeamService,
)

router = APIRouter(
    prefix="/projects/{project_id}/teams",
    tags=["Project Teams"],
)


@router.post(
    "",
    response_model=ProjectTeamResponse,
)
def assign_team(
    project_id: int,
    payload: ProjectTeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProjectTeamService.assign_team(
        db=db,
        organization_id=current_user.organization_id,
        project_id=project_id,
        team_id=payload.team_id,
    )


@router.get(
    "",
    response_model=list[ProjectTeamResponse],
)
def list_project_teams(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProjectTeamService.list_project_teams(
        db=db,
        organization_id=current_user.organization_id,
        project_id=project_id,
    )


@router.delete(
    "/{team_id}",
    response_model=ProjectTeamResponse,
)
def remove_project_team(
    project_id: int,
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProjectTeamService.remove_team(
        db=db,
        organization_id=current_user.organization_id,
        project_id=project_id,
        team_id=team_id,
    )
