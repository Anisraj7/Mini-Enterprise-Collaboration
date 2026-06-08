from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_roles
from app.db.database import get_db

from app.models.enums import UserRole

from app.schemas.tenant_onboarding import (
    TenantAdminCreate,
    TenantOnboardRequest,
    TenantOnboardingOut,
)

from app.services.tenant_onboarding_service import (
    TenantOnboardingService,
)

from app.core.dependencies import (
    get_current_user,
)

router = APIRouter()

super_admin_only = Depends(
    require_roles(
        [UserRole.SUPER_ADMIN.value]
    )
)


# Public onboarding endpoint - create organization + admin
@router.post(
    "/onboard",
    response_model=TenantOnboardingOut,
)
def onboard_tenant(
    payload: TenantOnboardRequest,
    db: Session = Depends(get_db),
):
    return TenantOnboardingService.onboard_tenant(
        db,
        payload,
    )


# Create an admin for an existing organization (super-admin only)
@router.post(
    "/{organization_id}/admin",
    response_model=TenantOnboardingOut,
)
def create_organization_admin(
    organization_id: int,
    payload: TenantAdminCreate,
    db: Session = Depends(get_db),
    current_user=super_admin_only,
):
    return TenantOnboardingService.create_admin(
        db,
        organization_id,
        payload,
    )


# Get onboarding status for an organization (authenticated users)
@router.get(
    "/{organization_id}/onboarding-status",
    response_model=TenantOnboardingOut,
)
def get_onboarding_status(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return TenantOnboardingService.get_status(
        db,
        organization_id,
    )