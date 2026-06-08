from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import Page
from fastapi_pagination import paginate
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.permissions import (
    require_manager_or_admin,
    require_roles,
)

from app.schemas.approval_escalation import (
    ApprovalEscalationCreate,
    ApprovalEscalationResponse,
)

from app.services.approval_escalation_service import (
    ApprovalEscalationService,
)

router = APIRouter(
    prefix="/approval-escalations",
    tags=["Approval Escalations"],
)


@router.post(
    "",
    response_model=ApprovalEscalationResponse,
)
def create_escalation(
    payload: ApprovalEscalationCreate,
    db: Session = Depends(get_db),
    user=Depends(require_manager_or_admin),
):
    return (
        ApprovalEscalationService.create_escalation(
            db=db,
            approval_id=payload.approval_id,
            escalated_from=user.id,
            escalated_to=payload.escalated_to,
            reason=payload.reason,
        )
    )


@router.get(
    "",
    response_model=Page[
        ApprovalEscalationResponse
    ],
)
def get_all_escalations(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            [
                "organization_admin",
                "workspace_admin",
                "manager",
            ]
        )
    ),
):
    return paginate(ApprovalEscalationService.get_all_escalations(db))


@router.get(
    "/pending",
    response_model=Page[
        ApprovalEscalationResponse
    ],
)
def get_pending_escalations(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            [
                "organization_admin",
                "workspace_admin",
                "manager",
            ]
        )
    ),
):
    return paginate(ApprovalEscalationService.get_pending_escalations(db))


@router.get(
    "/approval/{approval_id}",
    response_model=Page[
        ApprovalEscalationResponse
    ],
)
def get_escalation_history(
    approval_id: int,
    db: Session = Depends(get_db),
    user=Depends(
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
        ApprovalEscalationService.get_escalation_history(
            db,
            approval_id,
        )
    )


@router.put(
    "/{escalation_id}/resolve",
    response_model=ApprovalEscalationResponse,
)
def resolve_escalation(
    escalation_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_manager_or_admin),
):
    return (
        ApprovalEscalationService.resolve_escalation(
            db,
            escalation_id,
        )
    )


@router.put(
    "/{escalation_id}/cancel",
    response_model=ApprovalEscalationResponse,
)
def cancel_escalation(
    escalation_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_manager_or_admin),
):
    return (
        ApprovalEscalationService.cancel_escalation(
            db,
            escalation_id,
        )
    )
