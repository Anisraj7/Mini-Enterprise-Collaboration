from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
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


def get_document_by_id(
    db: Session,
    document_id: int,
):

    return (
        db.execute(select(Document).where(Document.id == document_id))
        .scalars()
        .first()
    )


def get_existing_document(
    db: Session,
    file_name: str,
    task_id: int,
):

    return (
        db.execute(select(Document).where(
            Document.file_name == file_name,
            Document.task_id == task_id,
        )
        .order_by(Document.version.desc())
        )
        .scalars()
        .first()
    )


def documents_query(
    db: Session,
    task_id: int,
):

    return (
        select(Document)
        .where(Document.task_id == task_id)
        .order_by(Document.created_at.desc())
    )


def create_document_repository(
    db: Session,
    document: Document,
):

    db.add(document)

    db.flush()

    return document


def commit_refresh(
    db: Session,
    model,
):

    db.commit()

    db.refresh(model)

    return model
