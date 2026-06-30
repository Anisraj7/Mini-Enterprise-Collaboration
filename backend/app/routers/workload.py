from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.services.workload_service import (
    WorkloadService,
)

router = APIRouter(
    tags=["Workload"],
)


@router.get(
    "/teams/{team_id}/workload"
)
def get_team_workload(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return WorkloadService.get_team_workload(
        db=db,
        team_id=team_id,
        organization_id=current_user.organization_id,
    )


@router.get(
    "/projects/{project_id}/workload"
)
def get_project_workload(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return WorkloadService.get_project_workload(
        db=db,
        organization_id=current_user.organization_id,
        project_id=project_id,
    )