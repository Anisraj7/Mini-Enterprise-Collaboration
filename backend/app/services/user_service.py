from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.cache import cache_get, cache_set
from app.models.user import User
from app.repository.user_repository import (
    get_users_query,
    get_user_by_id,
    get_assignable_users_query,
)

def get_all_users_service(db: Session, current_user: User):
    cache_key = f"users:list:{current_user.organization_id}"

    cached = cache_get(cache_key)
    if cached:
        return cached

    users = (
        get_users_query(db, current_user.organization_id)
        .order_by(User.name.asc())
        .all()
    )

    result = jsonable_encoder(users)

    cache_set(cache_key, result)

    return result


def get_assignable_users_service(db: Session, current_user: User):
    cache_key = f"users:assignable:{current_user.organization_id}"

    cached = cache_get(cache_key)
    if cached:
        return cached

    users = (
        get_assignable_users_query(db, current_user)
        .order_by(User.name.asc())
        .all()
    )

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

    if (
        current_user.organization_id
        and user.organization_id != current_user.organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    result = jsonable_encoder(user)

    cache_set(cache_key, result)

    return result

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.core.cache import invalidate_read_caches

from app.core.security import hash_password

from app.models.user import User
from app.models.organization import Organization

from app.schemas.user import UserCreate

from app.repository.auth_repository import (
    get_user_by_email,
    get_user_with_organization,
    get_organization_by_name,
    create_organization_repository,
    create_user_repository,
    commit_refresh,
)


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

    organization_id = user.organization_id

    if user.organization_name:

        organization = get_organization_by_name(
            db,
            user.organization_name,
        )

        if not organization:

            organization = Organization(
                name=user.organization_name,
                email=user.email if user.role.value == "admin" else None,
                plan="basic",
            )

            create_organization_repository(
                db,
                organization,
            )

        organization_id = organization.id

    new_user = User(
        name=user.name,
        email=user.email,
        role=user.role.value,
        hashed_password=hash_password(user.password),
        organization_id=organization_id,
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

    return get_user_with_organization(
        db,
        current_user.id,
    )