from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.approval import Approval
from app.models.task import Task

from app.repository.task_repository import visible_tasks_query


def approval_query(
    db: Session,
    user,
):

    query = select(Approval).where(
        Approval.status == "pending"
    )

    if user.organization_id:
        query = query.where(
            Approval.organization_id == user.organization_id
        )

    if user.role == "employee":
        query = query.where(
            Approval.requested_by == user.id
        )

    return query


def grouped_task_status_query(
    db: Session,
    query,
):

    grouped = query.with_only_columns(
        Task.status,
        func.count(Task.id),
    ).group_by(Task.status)

    return db.execute(grouped).all()


def grouped_approval_status_query(
    db: Session,
    user,
):

    query = select(
        Approval.status,
        func.count(Approval.id),
    )

    if user.organization_id:
        query = query.where(
            Approval.organization_id == user.organization_id
        )

    return db.execute(
        query.group_by(
            Approval.status
        )
    ).all()
