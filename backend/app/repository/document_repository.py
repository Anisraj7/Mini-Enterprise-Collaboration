from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.task import Task


def get_task_by_id(
    db: Session,
    task_id: int,
):

    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )


def get_document_by_id(
    db: Session,
    document_id: int,
):

    return (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )


def get_existing_document(
    db: Session,
    file_name: str,
    task_id: int,
):

    return (
        db.query(Document)
        .filter(
            Document.file_name == file_name,
            Document.task_id == task_id,
        )
        .order_by(Document.version.desc())
        .first()
    )


def documents_query(
    db: Session,
    task_id: int,
):

    return (
        db.query(Document)
        .filter(Document.task_id == task_id)
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
