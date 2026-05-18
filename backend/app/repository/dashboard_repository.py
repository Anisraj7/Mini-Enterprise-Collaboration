from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.approval import Approval
from app.models.task import Task

from app.repository.task_repository import visible_tasks_query


def approval_query(
    db: Session,
    user,
):

    query = db.query(Approval).filter(
        Approval.status == "pending"
    )

    if user.organization_id:
        query = query.filter(
            Approval.organization_id == user.organization_id
        )

    if user.role == "employee":
        query = query.filter(
            Approval.requested_by == user.id
        )

    return query


def grouped_task_status_query(
    query,
):

    return (
        query.with_entities(
            Task.status,
            func.count(Task.id),
        )
        .group_by(Task.status)
        .all()
    )


def grouped_approval_status_query(
    db: Session,
    user,
):

    query = db.query(
        Approval.status,
        func.count(Approval.id),
    )

    if user.organization_id:
        query = query.filter(
            Approval.organization_id == user.organization_id
        )

    return (
        query.group_by(
            Approval.status
        )
        .all()
    )