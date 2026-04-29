from app.services.task_service import get_kanban_board, apply_task_status


def update_task_status(task_id: int, new_status: str, user, db):
    from fastapi import HTTPException, status
    from app.models.task import Task

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    apply_task_status(task, new_status, user, db)
    db.commit()
    db.refresh(task)
    return task
