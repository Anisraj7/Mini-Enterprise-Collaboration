from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.models.audit import AuditLog
from app.models.comments import Comment
from app.models.task import Task
from app.services.notification_service import create_notification
from app.services.task_service import can_access_task


def create_comment(task_id: int, data, user, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if not can_access_task(task, user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    if data.is_internal and user.role == "employee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Employees cannot add internal comments")

    comment = Comment(
        task_id=task_id,
        user_id=user.id,
        content=data.content,
        is_internal=bool(data.is_internal),
    )
    db.add(comment)
    db.flush()
    db.add(ActivityLog(user_id=user.id, action="COMMENT_ADDED", entity_type="COMMENT", entity_id=comment.id))
    db.add(AuditLog(user_id=user.id, action="COMMENT_ADDED", entity="COMMENT", entity_id=comment.id))
    for recipient_id in {task.created_by_id, task.assigned_to_id} - {None, user.id}:
        create_notification(db, recipient_id, f"New comment on task: {task.title}")
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(task_id: int, user, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if not can_access_task(task, user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

    query = db.query(Comment).filter(Comment.task_id == task_id)
    if user.role == "employee":
        query = query.filter(Comment.is_internal.is_(False))
    return query.order_by(Comment.created_at.desc()).all()
