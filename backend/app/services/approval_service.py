from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.models.approval import Approval
from app.models.approval_history import ApprovalHistory
from app.models.user import User

APPROVAL_ACTIONS = ("approve", "reject", "hold")
FINAL_STATUSES = ("approved", "rejected")


def normalize_action(action: str) -> str:
    value = str(action).strip().lower()
    aliases = {"approved": "approve", "rejected": "reject", "held": "hold"}
    value = aliases.get(value, value)
    if value not in APPROVAL_ACTIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid approval action")
    return value


def create_approval(data, user: User, db: Session):
    approval = Approval(
        title=data.title,
        description=data.description,
        requested_by=user.id,
        status="pending",
        current_level="manager",
    )
    db.add(approval)
    db.flush()
    db.add(ActivityLog(user_id=user.id, action="APPROVAL_SUBMITTED", entity_type="APPROVAL", entity_id=approval.id))
    db.commit()
    db.refresh(approval)
    return approval


def take_action(approval_id: int, data, user: User, db: Session):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval not found")

    if approval.status in FINAL_STATUSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Approval is already finalized")

    action = normalize_action(data.action)
    comment = (data.comment or "").strip() or None

    if user.role not in ("manager", "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only managers or admins can act on approvals")

    if approval.current_level == "manager" and user.role not in ("manager", "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager approval is required")

    if approval.current_level == "admin" and user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin approval is required")

    if action == "reject" and not comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment required for rejection")

    if action == "approve":
        if approval.current_level == "manager" and user.role == "manager":
            approval.current_level = "admin"
            approval.status = "pending"
        else:
            approval.status = "approved"
    elif action == "reject":
        approval.status = "rejected"
    elif action == "hold":
        approval.status = "pending"

    db.add(
        ApprovalHistory(
            approval_id=approval.id,
            action_by=user.id,
            action=action,
            comment=comment,
        )
    )
    db.add(
        ActivityLog(
            user_id=user.id,
            action=f"APPROVAL_{action.upper()}",
            entity_type="APPROVAL",
            entity_id=approval.id,
        )
    )
    db.commit()
    db.refresh(approval)
    return approval


def get_approvals(user: User, db: Session):
    query = db.query(Approval)
    if user.role == "employee":
        query = query.filter(Approval.requested_by == user.id)
    return query.order_by(Approval.created_at.desc()).all()


def get_history(approval_id: int, user: User, db: Session):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval not found")
    if user.role == "employee" and approval.requested_by != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return (
        db.query(ApprovalHistory)
        .filter(ApprovalHistory.approval_id == approval_id)
        .order_by(ApprovalHistory.created_at.desc())
        .all()
    )
