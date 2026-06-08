from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.core.permissions import (
    get_current_user,
    require_roles,
)

from app.db.database import get_db

from app.models.user import User
from app.repository.user_repository import (
    get_assignable_users_query,
    get_users_query,
)

from app.schemas.user import (
    UserOut,
    UserSummary,
    OrganizationUserCreate,
    UserOut,
)

from app.services.user_service import (
    get_user_by_id_service,
    activate_user_service,
    deactivate_user_service,
    create_user_service,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post(
    "/",
    response_model=UserOut,
    status_code=201,
)
def create_user(
    payload: OrganizationUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            [
                "organization_admin",
            ]
        )
    ),
):
    return create_user_service(
        db,
        current_user,
        payload,
    )

from sqlalchemy import select

@router.get(
    "/",
    response_model=Page[UserSummary],
)
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "super_admin":

        query = (
            select(User)
            .where(
                User.role == "organization_admin"
            )
            .order_by(User.name.asc())
        )

        return paginate(db, query)

    if current_user.role == "organization_admin":

        return paginate(
            db,
            get_users_query(
                db,
                current_user.organization_id,
            ).order_by(User.name.asc()),
        )

    raise HTTPException(
        status_code=403,
        detail="Insufficient permissions",
    )


@router.get(
    "/assignable",
    response_model=Page[UserSummary],
)
def list_assignable_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            [
                "organization_admin",
                "workspace_admin",
                "manager",
            ]
        )
    ),
):
    return paginate(
        db,
        get_assignable_users_query(
            db,
            current_user,
        ).order_by(User.name.asc()),
    )


@router.get(
    "/{user_id}",
    response_model=UserOut,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_user_by_id_service(
        db,
        current_user,
        user_id,
    )

@router.patch(
    "/{user_id}/activate",
    response_model=UserOut,
)
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            ["organization_admin"]
        )
    ),
):
    return activate_user_service(
        db,
        current_user,
        user_id,
    )
    
@router.patch(
    "/{user_id}/deactivate",
    response_model=UserOut,
)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            ["organization_admin"]
        )
    ),
):
    return deactivate_user_service(
        db,
        current_user,
        user_id,
    )