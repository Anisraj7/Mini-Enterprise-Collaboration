from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
)

from app.db.database import get_db

from app.schemas.approval_delegation import (
    ApprovalDelegationCreate,
    ApprovalDelegationOut,
)

from app.services.approval_delegation_service import (
    ApprovalDelegationService,
)

router = APIRouter(
    prefix="/approval-delegations",
    tags=["Approval Delegations"],
)


@router.post(
    "/",
    response_model=ApprovalDelegationOut,
)
def create_delegation(
    payload: ApprovalDelegationCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return (
        ApprovalDelegationService.create_delegation(
            db,
            user,
            payload,
        )
    )


@router.get(
    "/me",
    response_model=list[
        ApprovalDelegationOut
    ],
)
def get_my_delegations(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return (
        ApprovalDelegationService.get_my_delegations(
            db,
            user,
        )
    )


@router.get(
    "/active",
    response_model=list[
        ApprovalDelegationOut
    ],
)
def get_active_delegations(
    db: Session = Depends(get_db),
):
    return (
        ApprovalDelegationService.get_active_delegations(
            db
        )
    )


@router.put(
    "/{delegation_id}/cancel",
    response_model=ApprovalDelegationOut,
)
def cancel_delegation(
    delegation_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return (
        ApprovalDelegationService.cancel_delegation(
            db,
            delegation_id,
            user,
        )
    )