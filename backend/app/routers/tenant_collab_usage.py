from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.core.permissions import require_roles
from app.db.database import get_db

from app.models.enums import UserRole

from app.schemas.tenant_collab_usage import (
    TenantCollaborationUsageResponse,
)

from app.services.tenant_collab_usage_service import (
    TenantCollaborationUsageService,
)

router = APIRouter()

tenant_admin_access = Depends(
    require_roles(
        [
            UserRole.SUPER_ADMIN.value,
            UserRole.ORGANIZATION_ADMIN.value,
        ]
    )
)


@router.get(
    "/{organization_id}/usage",
    response_model=TenantCollaborationUsageResponse,
)
def get_collaboration_usage(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user=tenant_admin_access,
):
    return TenantCollaborationUsageService.get_usage(
        db,
        organization_id,
        current_user,
    )


@router.post(
    "/{organization_id}/recalculate-usage",
    response_model=TenantCollaborationUsageResponse,
)
def recalculate_collaboration_usage(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user=tenant_admin_access,
):
    return TenantCollaborationUsageService.recalculate_usage(
        db,
        organization_id,
        current_user,
    )