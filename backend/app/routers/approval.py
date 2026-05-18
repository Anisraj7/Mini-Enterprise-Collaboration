from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.core.dependencies import get_current_user

from app.db.database import get_db

from app.models.user import User

from app.schemas.approval import (
    ApprovalAction,
    ApprovalCreate,
    ApprovalHistoryOut,
    ApprovalOut,
)

from app.services.approval_service import (
    create_approval_service,
    get_approvals_service,
    get_history_service,
    take_action_service,
)

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"],
)


@router.post(
    "/",
    response_model=ApprovalOut,
)
def create(
    payload: ApprovalCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return create_approval_service(
        payload,
        user,
        db,
    )


@router.get(
    "/",
    response_model=Page[ApprovalOut],
)
def list_all(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return get_approvals_service(
        user,
        db,
    )


@router.patch(
    "/{approval_id}/action",
    response_model=ApprovalOut,
)
def action(
    approval_id: int,
    payload: ApprovalAction,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return take_action_service(
        approval_id,
        payload,
        user,
        db,
    )


@router.get(
    "/{approval_id}/history",
    response_model=Page[ApprovalHistoryOut],
)
def history(
    approval_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return get_history_service(
        approval_id,
        user,
        db,
    )