from fastapi import (
    APIRouter,
    Depends, HTTPException, status
)
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.core.permissions import require_roles
from app.db.database import get_db

from app.models.enums import UserRole
from app.repository.organization_repository import OrganizationRepository

from app.schemas.organization import (
    OrganizationCreate,
    OrganizationOut,
    OrganizationUpdate,
)

from app.services.organization_service import (
    OrganizationService,
)

from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter()

super_admin_only = Depends(
    require_roles(
        [UserRole.SUPER_ADMIN.value]
    )
)


@router.post(
    "",
    response_model=OrganizationOut
)
def create_organization(
    payload: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user=super_admin_only,
):
    return OrganizationService.create_organization(
        db,
        payload
    )


@router.get(
    "",
    response_model=Page[OrganizationOut]
)
def list_organizations(
    db: Session = Depends(get_db),
    current_user=super_admin_only,
):
    return paginate(db, OrganizationRepository.get_all_stmt(db))


@router.get(
    "/{organization_id}",
    response_model=OrganizationOut
)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    if current_user.role != UserRole.SUPER_ADMIN.value:
        if (
            current_user.role
            != UserRole.ORGANIZATION_ADMIN.value
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        if (
            current_user.organization_id
            != organization_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

    return OrganizationService.get_organization(
        db,
        organization_id,
    )


@router.put(
    "/{organization_id}",
    response_model=OrganizationOut
)
def update_organization(
    organization_id: int,
    payload: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user=super_admin_only,
):
    return OrganizationService.update_organization(
        db,
        organization_id,
        payload
    )


@router.patch(
    "/{organization_id}/suspend",
    response_model=OrganizationOut
)
def suspend_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user=super_admin_only,
):
    return OrganizationService.suspend_organization(
        db,
        organization_id
    )

@router.delete("/{organization_id}")
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user=super_admin_only,
):
    return OrganizationService.delete_organization(
        db,
        organization_id
    )

@router.patch(
    "/{organization_id}/activate",
    response_model=OrganizationOut
)
def activate_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user=super_admin_only,
):
    return OrganizationService.activate_organization(
        db,
        organization_id
    )
