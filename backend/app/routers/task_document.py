from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException,
)

from fastapi.responses import FileResponse

from fastapi_pagination import Page

from app.db.database import get_db

from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.task_document import (
    TaskDocumentResponse,
)

from app.services.task_document_service import (
    TaskDocumentService,
)

router = APIRouter(
    prefix="/tasks",
    tags=["Task Documents"],
)


@router.post(
    "/{task_id}/documents",
    response_model=TaskDocumentResponse,
)
def upload_task_document(
    task_id: int,
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return TaskDocumentService.upload_document(
        db=db,
        organization_id=current_user.organization_id,
        task_id=task_id,
        uploaded_by=current_user.id,
        file=file,
        document_type=document_type,
    )


@router.get(
    "/{task_id}/documents",
    response_model=Page[TaskDocumentResponse],
)
def list_task_documents(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return TaskDocumentService.list_documents(
        db=db,
        task_id=task_id,
    )


@router.get(
    "/documents/{document_id}/download",
)
def download_task_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    document = TaskDocumentService.get_document(
        db=db,
        document_id=document_id,
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return FileResponse(
        path=document.file_path,
        filename=document.file_name,
        media_type=document.mime_type,
    )


@router.delete(
    "/documents/{document_id}",
)
def delete_task_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    document = TaskDocumentService.get_document(
        db=db,
        document_id=document_id,
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    TaskDocumentService.delete_document(
        db=db,
        document=document,
    )

    return {
        "message": "Document deleted successfully",
    }