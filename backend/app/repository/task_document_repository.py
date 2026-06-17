from __future__ import annotations

from sqlalchemy import (
    delete,
    select,
)

from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.task_document import TaskDocument


class TaskDocumentRepository:

    @staticmethod
    def create(
        db: Session,
        document: TaskDocument,
    ) -> TaskDocument:

        db.add(document)

        db.commit()

        db.refresh(document)

        return document

    @staticmethod
    def get_by_id(
        db: Session,
        document_id: int,
    ) -> TaskDocument | None:

        stmt = (
            select(TaskDocument)
            .where(
                TaskDocument.id == document_id
            )
        )

        result = db.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    def list_by_task(
        db: Session,
        task_id: int,
    ):

        stmt = (
            select(TaskDocument)
            .where(
                TaskDocument.task_id == task_id
            )
            .order_by(
                TaskDocument.created_at.desc()
            )
        )

        return paginate(
            db,
            stmt,
        )

    @staticmethod
    def get_by_task_and_file_name(
        db: Session,
        task_id: int,
        file_name: str,
    ) -> TaskDocument | None:

        stmt = (
            select(TaskDocument)
            .where(
                TaskDocument.task_id == task_id
            )
            .where(
                TaskDocument.file_name == file_name
            )
        )

        result = db.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    def delete(
        db: Session,
        document: TaskDocument,
    ) -> None:

        db.delete(document)

        db.commit()

    @staticmethod
    def delete_by_id(
        db: Session,
        document_id: int,
    ) -> None:

        stmt = (
            delete(TaskDocument)
            .where(
                TaskDocument.id == document_id
            )
        )

        db.execute(stmt)

        db.commit()