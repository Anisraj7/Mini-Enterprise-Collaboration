import os
import uuid

from fastapi import (
    UploadFile,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.models.project_document import (
    ProjectDocument
)

from app.repository.project_document_repository import (
    ProjectDocumentRepository
)

from app.services.project_service import (
    ProjectService
)


UPLOAD_DIR = "uploads/projects"


class ProjectDocumentService:

    @staticmethod
    async def upload_document(
        db: Session,
        organization_id: int,
        user_id: int,
        project_id: int,
        document_type,
        file: UploadFile
    ):

        project = ProjectService.get_project(
            db,
            organization_id,
            project_id
        )

        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True
        )

        filename = (
            f"{uuid.uuid4()}_{file.filename}"
        )

        filepath = os.path.join(
            UPLOAD_DIR,
            filename
        )

        content = await file.read()

        with open(filepath, "wb") as buffer:
            buffer.write(content)

        document = ProjectDocument(
            organization_id=organization_id,
            project_id=project.id,
            file_name=file.filename,
            file_path=filepath,
            file_size=len(content),
            mime_type=file.content_type,
            uploaded_by=user_id,
            document_type=document_type
        )

        return ProjectDocumentRepository.create(
            db,
            document
        )

    @staticmethod
    def list_documents(
        db: Session,
        organization_id: int,
        project_id: int
    ):

        ProjectService.get_project(
            db,
            organization_id,
            project_id
        )

        return (
            ProjectDocumentRepository
            .get_project_documents(
                db,
                project_id
            )
        )

    @staticmethod
    def get_document(
        db: Session,
        organization_id: int,
        document_id: int
    ):

        document = (
            ProjectDocumentRepository
            .get_by_id(
                db,
                document_id,
                organization_id
            )
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        return document