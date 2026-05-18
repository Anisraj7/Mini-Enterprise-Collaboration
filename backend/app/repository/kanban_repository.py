from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User


def get_task_by_id(
    db: Session,
    task_id: int,
):

    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )


def active_workspace_users_query(
    db: Session,
    user,
):

    query = db.query(User.id).filter(
        User.is_active.is_(True)
    )

    if user.organization_id:
        query = query.filter(
            User.organization_id
            == user.organization_id
        )

    return query.all()


def commit_refresh(
    db: Session,
    model,
):

    db.commit()

    db.refresh(model)

    return model