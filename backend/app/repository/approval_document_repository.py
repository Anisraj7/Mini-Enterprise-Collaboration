from __future__ import annotations

from sqlalchemy import (
    delete,
    select,
)

from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.approval_document import ApprovalDocument


class ApprovalDocumentRepository:

    @staticmethod
    def create(
        db: Session,
        document: ApprovalDocument,
    ) -> ApprovalDocument:

        db.add(document)

        db.commit()

        db.refresh(document)

        return document

    @staticmethod
    def get_by_id(
        db: Session,
        document_id: int,
    ) -> ApprovalDocument | None:

        stmt = (
            select(ApprovalDocument)
            .where(
                ApprovalDocument.id == document_id
            )
        )

        result = db.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    def list_by_approval(
        db: Session,
        approval_id: int,
    ):

        stmt = (
            select(ApprovalDocument)
            .where(
                ApprovalDocument.approval_id == approval_id
            )
            .order_by(
                ApprovalDocument.created_at.desc()
            )
        )

        return paginate(
            db,
            stmt,
        )

    @staticmethod
    def get_by_approval_and_file_name(
        db: Session,
        approval_id: int,
        file_name: str,
    ) -> ApprovalDocument | None:

        stmt = (
            select(ApprovalDocument)
            .where(
                ApprovalDocument.approval_id == approval_id
            )
            .where(
                ApprovalDocument.file_name == file_name
            )
        )

        result = db.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    def delete(
        db: Session,
        document: ApprovalDocument,
    ) -> None:

        db.delete(document)

        db.commit()

    @staticmethod
    def delete_by_id(
        db: Session,
        document_id: int,
    ) -> None:

        stmt = (
            delete(ApprovalDocument)
            .where(
                ApprovalDocument.id == document_id
            )
        )

        db.execute(stmt)

        db.commit()

    @staticmethod
    def exists(
        db: Session,
        document_id: int,
    ) -> bool:

        stmt = (
            select(ApprovalDocument.id)
            .where(
                ApprovalDocument.id == document_id
            )
        )

        result = db.execute(stmt)

        return result.scalar_one_or_none() is not None