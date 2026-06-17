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

from app.schemas.approval_document import (
    ApprovalDocumentResponse,
)

from app.services.approval_document_service import (
    ApprovalDocumentService,
)

router = APIRouter(
    prefix="/approvals",
    tags=["Approval Documents"],
)


@router.post(
    "/{approval_id}/documents",
    response_model=ApprovalDocumentResponse,
)
def upload_approval_document(
    approval_id: int,
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return ApprovalDocumentService.upload_document(
        db=db,
        organization_id=current_user.organization_id,
        approval_id=approval_id,
        uploaded_by=current_user.id,
        file=file,
        document_type=document_type,
    )


@router.get(
    "/{approval_id}/documents",
    response_model=Page[ApprovalDocumentResponse],
)
def list_approval_documents(
    approval_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return ApprovalDocumentService.list_documents(
        db=db,
        approval_id=approval_id,
    )


@router.get(
    "/documents/{document_id}/download",
)
def download_approval_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    document = ApprovalDocumentService.get_document(
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
def delete_approval_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    document = ApprovalDocumentService.get_document(
        db=db,
        document_id=document_id,
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    ApprovalDocumentService.delete_document(
        db=db,
        document=document,
    )

    return {
        "message": "Document deleted successfully",
    }