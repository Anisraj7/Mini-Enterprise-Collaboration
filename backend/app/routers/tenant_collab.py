from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.dependencies import (
    get_current_user,
)

from app.schemas.tenant_collab_settings import (
    TenantCollaborationSettingsResponse,
    TenantCollaborationSettingsUpdate,
)

from app.services.tenant_collab_settings_service import (
    TenantCollaborationSettingsService,
)

router = APIRouter()


@router.get(
    "/{organization_id}/collaboration/settings",
    response_model=TenantCollaborationSettingsResponse,
)
def get_collaboration_settings(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return TenantCollaborationSettingsService.get_settings(
        db,
        organization_id,
        current_user,
    )


@router.put(
    "/{organization_id}/collaboration/settings",
    response_model=TenantCollaborationSettingsResponse,
)
def update_collaboration_settings(
    organization_id: int,
    payload: TenantCollaborationSettingsUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return TenantCollaborationSettingsService.update_settings(
        db,
        organization_id,
        payload,
        current_user,
    )