from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.permissions import get_current_user, require_roles
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserSummary
from app.services.user_service import (
    get_all_users_service,
    get_assignable_users_service,
    get_user_by_id_service,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserSummary])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
):
    return get_all_users_service(db, current_user)


@router.get("/assignable", response_model=list[UserSummary])
def list_assignable_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin", "manager"])),
):
    return get_assignable_users_service(db, current_user)


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_by_id_service(db, current_user, user_id)