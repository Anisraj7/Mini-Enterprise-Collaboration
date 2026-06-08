from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.cache import (
    cache_get,
    cache_set,
    invalidate_read_caches,
)

from app.models.approval import (
    Approval,
    ApprovalHistory,
)

from app.models.user import User

from app.schemas.approval import (
    ApprovalAction,
    ApprovalCreate,
)

from app.services.notification_service import (
    create_notification,
)

from app.services.sla_tracking_service import (
    SLATrackingService,
)

from app.repository.approval_repository import (
    create_approval_repository,
    create_approval_history_repository,
    get_approval_by_id,
    approvals_query,
    approval_history_query,
    commit_refresh,
)


def create_approval_service(
    payload: ApprovalCreate,
    user,
    db: Session,
):

    approval = Approval(
        title=payload.title,
        description=payload.description,
        requested_by=user.id,
        status="pending",
        organization_id=user.organization_id,
    )

    create_approval_repository(
        db,
        approval,
    )

    try:
        SLATrackingService.start_sla_tracking(
            db,
            "Approval",
            approval.id,
            "Medium",
        )

        db.refresh(
            approval,
        )

    except HTTPException:
        pass

    approvers = (
        db.execute(select(User).where(
            User.organization_id == user.organization_id,
            User.role.in_(
                [
                    "organization_admin",
                    "workspace_admin",
                    "manager",
                ]
            ),
            User.id != user.id,
            User.is_active.is_(True),
        ))
        .scalars()
        .all()
    )

    for approver in approvers:

        create_notification(
            db,
            approver.id,
            f"New approval request: {payload.title}",
            user.organization_id,
        )

    commit_refresh(
        db,
        approval,
    )

    invalidate_read_caches()

    return approval


def get_approvals_service(
    user,
    db: Session,
):

    cache_key = (
        f"approvals:list:"
        f"user:{user.id}:"
        f"role:{user.role}"
    )

    cached = cache_get(
        cache_key,
    )

    if cached:
        return cached

    query = approvals_query(
        db,
        user,
    )

    result = paginate(db, query)

    result = jsonable_encoder(
        result,
    )

    cache_set(
        cache_key,
        result,
    )

    return result


def take_action_service(
    approval_id: int,
    payload: ApprovalAction,
    user,
    db: Session,
):

    approval = get_approval_by_id(
        db,
        approval_id,
    )

    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval not found",
        )

    if approval.organization_id != user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval not found",
        )

    if approval.status in {
        "approved",
        "rejected",
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Approval is already closed",
        )

    can_act = (
        user.role in (
            "super_admin",
            "organization_admin",
            "workspace_admin",
        )
        or (
            user.role == "manager"
            and approval.current_level == "manager"
        )
    )

    if not can_act:

        try:
            from app.repository.approval_delegation_repository import (
                ApprovalDelegationRepository,
            )

            active_delegations = (
                ApprovalDelegationRepository.get_active(
                    db,
                )
            )

            delegatee_id = user.id

            for delegation in active_delegations:

                if delegation.delegatee_id != delegatee_id:
                    continue

                if (
                    approval.current_level
                    == "manager"
                ):
                    can_act = True
                    break

        except Exception:
            pass

    if approval.is_escalated:

        if (
            approval.current_escalation_to is None
            or user.id != approval.current_escalation_to
        ):
            can_act = False

    if not can_act:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed",
        )

    if (
        payload.action == "reject"
        and not (payload.comment or "").strip()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment required for rejection",
        )

    status_by_action = {
        "approve": "approved",
        "reject": "rejected",
        "hold": "hold",
    }

    approval.status = status_by_action[
        payload.action
    ]

    if approval.status in {
        "approved",
        "rejected",
    }:
        try:

            tracking = (
                SLATrackingService.get_sla_record(
                    db,
                    "Approval",
                    approval.id,
                )
            )

            if (
                tracking
                and not tracking.completed_time
            ):
                SLATrackingService.complete_sla(
                    db,
                    tracking.id,
                )

                db.refresh(
                    approval,
                )

        except HTTPException:
            pass

    history = ApprovalHistory(
        approval_id=approval.id,
        action=payload.action,
        comment=payload.comment,
        action_by=user.id,
        organization_id=user.organization_id,
    )

    create_approval_history_repository(
        db,
        history,
    )

    create_notification(
        db,
        approval.requested_by,
        f"Approval {payload.action}: {approval.title}",
        user.organization_id,
    )

    commit_refresh(
        db,
        approval,
    )

    invalidate_read_caches()

    return approval


def get_history_service(
    approval_id: int,
    user,
    db: Session,
):

    cache_key = (
        f"approvals:history:"
        f"user:{user.id}:"
        f"approval:{approval_id}"
    )

    cached = cache_get(
        cache_key,
    )

    if cached:
        return cached

    approval = get_approval_by_id(
        db,
        approval_id,
    )

    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval not found",
        )

    if approval.organization_id != user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval not found",
        )

    if (
        user.role == "employee"
        and approval.requested_by != user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    query = approval_history_query(
        db,
        approval_id,
    )

    result = paginate(db, query)

    result = jsonable_encoder(
        result,
    )

    cache_set(
        cache_key,
        result,
    )

    return result
