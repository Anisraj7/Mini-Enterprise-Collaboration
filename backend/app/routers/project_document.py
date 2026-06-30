from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form
)

from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User

from app.enums.document import (
    ProjectDocumentType
)

from app.schemas.project_document import (
    ProjectDocumentResponse
)

from app.services.project_document_service import (
    ProjectDocumentService
)
from app.repository.project_document_repository import ProjectDocumentRepository

router = APIRouter(
    tags=["Project Documents"]
)

@router.post(
    "/projects/{project_id}/documents",
    response_model=ProjectDocumentResponse
)
async def upload_document(
    project_id: int,
    document_type: ProjectDocumentType = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await (
        ProjectDocumentService
        .upload_document(
            db=db,
            organization_id=current_user.organization_id,
            user_id=current_user.id,
            project_id=project_id,
            document_type=document_type,
            file=file
        )
    )
    
@router.get(
    "/projects/{project_id}/documents",
    response_model=list[ProjectDocumentResponse]
)
def list_documents(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProjectDocumentService.list_documents(
        db,
        organization_id=current_user.organization_id,
        project_id=project_id
    )

@router.get(
    "/project-documents/{document_id}/download"
)
def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        ProjectDocumentService.get_document(
            db,
            organization_id=current_user.organization_id,
            document_id=document_id
        )
    )

    return FileResponse(
        path=document.file_path,
        filename=document.file_name,
        media_type=document.mime_type
    )
    
@router.delete(
    "/project-documents/{document_id}"
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        ProjectDocumentService.get_document(
            db,
            organization_id=current_user.organization_id,
            document_id=document_id
        )
    )

    ProjectDocumentRepository.delete(
        db,
        document
    )

    return {
        "message": "Document deleted"
    }
