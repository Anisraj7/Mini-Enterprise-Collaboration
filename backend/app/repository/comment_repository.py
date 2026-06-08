from sqlalchemy import select
from sqlalchemy.orm import (
    Session,
    joinedload,
)

from app.models.comments import Comment
from app.models.task import Task


def get_task_by_id(
    db: Session,
    task_id: int,
):

    return (
        db.execute(select(Task).where(Task.id == task_id))
        .scalars()
        .first()
    )


def comments_query(
    db: Session,
    task_id: int,
    user,
):

    query = (
        select(Comment)
        .options(
            joinedload(Comment.user)
        )
        .where(
            Comment.task_id == task_id
        )
    )

    if user.role == "employee":
        query = query.where(
            Comment.is_internal.is_(False)
        )

    return query.order_by(
        Comment.created_at.desc()
    )


def create_comment_repository(
    db: Session,
    comment: Comment,
):

    db.add(comment)

    db.flush()

    return comment


def commit_refresh(
    db: Session,
    model,
):

    db.commit()

    db.refresh(model)

    return model
