from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

from app.schemas.team_member import (
    TeamMemberCreate,
    TeamMemberResponse,
)

from app.services.team_member_service import (
    TeamMemberService,
)

router = APIRouter(
    prefix="/teams/{team_id}/members",
    tags=["Team Members"],
)


@router.post(
    "",
    response_model=TeamMemberResponse,
)
def add_member(
    team_id: int,
    payload: TeamMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TeamMemberService.add_member(
        db=db,
        organization_id=current_user.organization_id,
        team_id=team_id,
        user_id=payload.user_id,
        role=payload.role,
    )


@router.get(
    "",
    response_model=list[TeamMemberResponse],
)
def list_members(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TeamMemberService.list_members(
        db=db,
        organization_id=current_user.organization_id,
        team_id=team_id,
    )


@router.delete("/{user_id}")
def remove_member(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    TeamMemberService.remove_member(
        db=db,
        organization_id=current_user.organization_id,
        team_id=team_id,
        user_id=user_id,
    )

    return {
        "message": "Team member removed successfully"
    }
    
    