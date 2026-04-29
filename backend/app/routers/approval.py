from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.approval import ApprovalAction, ApprovalCreate, ApprovalHistoryOut, ApprovalOut
from app.services.approval_service import create_approval, get_approvals, get_history, take_action

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.post("/", response_model=ApprovalOut)
def create(
    payload: ApprovalCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return create_approval(payload, user, db)


@router.get("/", response_model=List[ApprovalOut])
def list_all(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return get_approvals(user, db)


@router.patch("/{approval_id}/action", response_model=ApprovalOut)
def action(
    approval_id: int,
    payload: ApprovalAction,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return take_action(approval_id, payload, user, db)


@router.get("/{approval_id}/history", response_model=List[ApprovalHistoryOut])
def history(
    approval_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return get_history(approval_id, user, db)
