from typing import cast

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.cache import cache_get, cache_set, invalidate_read_caches
from app.core.security import hash_password
from app.models.user import User
from app.repository.auth_repository import (
    commit_refresh,
    create_user_repository,
    get_user_by_email,
    get_user_with_organization,
)
from app.repository.user_repository import (
    get_assignable_users_query,
    get_user_by_id,
    get_users_query,
)
from app.schemas.user import (
    UserCreate,
    OrganizationUserCreate,
    UserOut,
    UserRole,
)

def create_user_service(
    db: Session,
    current_user: User,
    payload: OrganizationUserCreate,
):
    existing_user = get_user_by_email(
        db,
        payload.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(
            payload.password
        ),
        role=payload.role.value,
        organization_id=current_user.organization_id,
        is_active=True,
    )

    create_user_repository(
        db,
        user,
    )

    commit_refresh(
        db,
        user,
    )

    invalidate_read_caches()

    return user


def get_all_users_service(db: Session, current_user: User):
    organization_id = cast(int | None, current_user.organization_id)
    cache_key = f"users:list:{organization_id}"

    cached = cache_get(cache_key)
    if cached:
        return cached

    users = db.execute(
        get_users_query(db, organization_id).order_by(User.name.asc())
    ).scalars().all()

    result = jsonable_encoder(users)

    cache_set(cache_key, result)

    return result


def get_assignable_users_service(db: Session, current_user: User):
    organization_id = cast(int | None, current_user.organization_id)
    cache_key = f"users:assignable:{organization_id}"

    cached = cache_get(cache_key)
    if cached:
        return cached

    users = db.execute(
        get_assignable_users_query(db, current_user).order_by(User.name.asc())
    ).scalars().all()

    result = jsonable_encoder(users)

    cache_set(cache_key, result)

    return result


def get_user_by_id_service(
    db: Session,
    current_user: User,
    user_id: int,
):
    cache_key = f"user:{user_id}"

    cached = cache_get(cache_key)
    if cached:
        return cached

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    current_user_organization_id = cast(
        int | None, current_user.__dict__.get("organization_id")
    )
    current_user_role = cast(str, current_user.__dict__.get("role"))
    current_user_id = cast(int, current_user.__dict__.get("id"))
    user_organization_id = cast(int | None, user.__dict__.get("organization_id"))

    if (
        current_user_organization_id is not None
        and user_organization_id != current_user_organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if (
        current_user_role
        not in [
            UserRole.ORGANIZATION_ADMIN.value,
            UserRole.SUPER_ADMIN.value,
        ]
        and current_user_id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    result = jsonable_encoder(user)

    cache_set(cache_key, result)

    return result


def register_service(
    db: Session,
    user: UserCreate,
):
    existing_user = get_user_by_email(
        db,
        user.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(
            user.password
        ),
        role=UserRole.EMPLOYEE.value,
        organization_id=None,
        is_active=True,
    )

    create_user_repository(
        db,
        new_user,
    )

    commit_refresh(
        db,
        new_user,
    )

    invalidate_read_caches()

    return new_user


def get_me_service(
    db: Session,
    current_user: User,
):
    current_user_id = cast(int, current_user.id)
    return get_user_with_organization(db, current_user_id)

def activate_user_service(
    db: Session,
    current_user: User,
    user_id: int,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if (
        user.organization_id
        != current_user.organization_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions",
        )

    user.is_active = True

    db.commit()
    db.refresh(user)

    return user

def deactivate_user_service(
    db: Session,
    current_user: User,
    user_id: int,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
        
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot deactivate your own account",
        )

    if (
        user.organization_id
        != current_user.organization_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions",
        )

    user.is_active = False

    db.commit()
    db.refresh(user)

    return user