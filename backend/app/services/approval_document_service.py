from __future__ import annotations

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.approval_document import ApprovalDocument

from app.repository.approval_document_repository import (
    ApprovalDocumentRepository,
)

from app.utils.file_storage import FileStorage
from app.utils.file_validator import FileValidator


class ApprovalDocumentService:

    @staticmethod
    def upload_document(
        db: Session,
        organization_id: int,
        approval_id: int,
        uploaded_by: int,
        file: UploadFile,
        document_type: str,
    ) -> ApprovalDocument:

        FileValidator.validate(file)

        file_path = FileStorage.save_approval_file(
            approval_id=approval_id,
            file=file,
        )

        file.file.seek(
            0,
            2,
        )

        file_size = file.file.tell()

        file.file.seek(0)

        document = ApprovalDocument(
            organization_id=organization_id,
            approval_id=approval_id,
            uploaded_by=uploaded_by,
            file_name=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type,
            document_type=document_type,
        )

        return ApprovalDocumentRepository.create(
            db=db,
            document=document,
        )

    @staticmethod
    def get_document(
        db: Session,
        document_id: int,
    ) -> ApprovalDocument | None:

        return ApprovalDocumentRepository.get_by_id(
            db=db,
            document_id=document_id,
        )

    @staticmethod
    def list_documents(
        db: Session,
        approval_id: int,
    ):

        return ApprovalDocumentRepository.list_by_approval(
            db=db,
            approval_id=approval_id,
        )

    @staticmethod
    def delete_document(
        db: Session,
        document: ApprovalDocument,
    ) -> None:

        FileStorage.delete_file(
            document.file_path
        )

        ApprovalDocumentRepository.delete(
            db=db,
            document=document,
        )