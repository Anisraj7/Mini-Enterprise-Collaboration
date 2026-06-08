from sqlalchemy import select
from sqlalchemy.orm import (
    Session,
    joinedload,
)

from app.models.approval import (
    Approval,
    ApprovalHistory,
)


def get_approval_by_id(
    db: Session,
    approval_id: int,
):

    return (
        db.execute(select(Approval).where(Approval.id == approval_id))
        .scalars()
        .first()
    )


def approvals_query(
    db: Session,
    user,
):

    query = select(Approval)

    if user.organization_id:
        query = query.where(
            Approval.organization_id
            == user.organization_id
        )

    if user.role == "employee":
        query = query.where(
            Approval.requested_by == user.id
        )

    return (
        query.options(
            joinedload(Approval.requester),
        )
        .order_by(Approval.created_at.desc())
    )


def approval_history_query(
    db: Session,
    approval_id: int,
):

    return (
        select(ApprovalHistory)
        .where(
            ApprovalHistory.approval_id
            == approval_id
        )
        .options(
            joinedload(ApprovalHistory.user)
        )
        .order_by(
            ApprovalHistory.created_at.desc()
        )
    )


def create_approval_repository(
    db: Session,
    approval: Approval,
):

    db.add(approval)

    db.flush()

    return approval


def create_approval_history_repository(
    db: Session,
    history: ApprovalHistory,
):

    db.add(history)

    return history


def commit_refresh(
    db: Session,
    model,
):

    db.commit()

    db.refresh(model)

    return model
