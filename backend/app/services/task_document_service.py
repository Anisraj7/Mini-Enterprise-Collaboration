from __future__ import annotations

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.task_document import TaskDocument

from app.repository.task_document_repository import (
    TaskDocumentRepository,
)

from app.utils.file_storage import FileStorage
from app.utils.file_validator import FileValidator


class TaskDocumentService:

    @staticmethod
    def upload_document(
        db: Session,
        organization_id: int,
        task_id: int,
        uploaded_by: int,
        file: UploadFile,
        document_type: str,
    ) -> TaskDocument:

        FileValidator.validate(file)

        file_path = FileStorage.save_task_file(
            task_id=task_id,
            file=file,
        )

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        document = TaskDocument(
            organization_id=organization_id,
            task_id=task_id,
            uploaded_by=uploaded_by,
            file_name=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type,
            document_type=document_type,
        )

        return TaskDocumentRepository.create(
            db=db,
            document=document,
        )

    @staticmethod
    def get_document(
        db: Session,
        document_id: int,
    ) -> TaskDocument | None:

        return TaskDocumentRepository.get_by_id(
            db=db,
            document_id=document_id,
        )

    @staticmethod
    def list_documents(
        db: Session,
        task_id: int,
    ):

        return TaskDocumentRepository.list_by_task(
            db=db,
            task_id=task_id,
        )

    @staticmethod
    def delete_document(
        db: Session,
        document: TaskDocument,
    ) -> None:

        FileStorage.delete_file(
            document.file_path
        )

        TaskDocumentRepository.delete(
            db=db,
            document=document,
        )