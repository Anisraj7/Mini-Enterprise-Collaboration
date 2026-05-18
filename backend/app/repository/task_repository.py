from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.task import Task
from app.models.user import User


def get_task_by_id(db: Session, task_id: int):
    return (
        db.query(Task)
        .options(joinedload(Task.assigned_to))
        .filter(Task.id == task_id)
        .first()
    )


def get_tasks_query(db: Session):
    return db.query(Task)


def visible_tasks_query(db: Session, user: User):

    query = db.query(Task)

    if user.organization_id:
        query = query.filter(
            Task.organization_id == user.organization_id
        )

    if user.role == "admin":
        return query

    if user.role == "manager":
        return query.filter(
            or_(
                Task.created_by_id == user.id,
                Task.assigned_to_id == user.id,
            )
        )

    return query.filter(
        Task.assigned_to_id == user.id
    )


def assignable_users_query(db: Session, user: User):

    query = db.query(User).filter(
        User.is_active.is_(True)
    )

    if user.organization_id:
        query = query.filter(
            User.organization_id == user.organization_id
        )

    if user.role == "manager":
        query = query.filter(
            User.role.in_(["manager", "employee"])
        )

    return query


def create_task_repository(db: Session, task: Task):

    db.add(task)

    db.flush()

    return task


def update_task_repository(db: Session, task: Task):

    db.add(task)

    return task


def delete_task_repository(db: Session, task: Task):

    db.delete(task)

    return True


def commit_refresh(db: Session, task: Task):

    db.commit()

    db.refresh(task)

    return task