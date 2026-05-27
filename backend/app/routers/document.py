from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    File,
    Request,
)

from fastapi.responses import FileResponse

from typing import Optional


from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.core.permissions import (
    get_current_user,
    require_roles,
)

from app.core.rate_limit import limiter

from app.db.database import get_db

from app.schemas.document import DocumentOut

from app.services.document_service import (
    upload_document_service,
    get_task_documents_service,
    get_document_service,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentOut,
)
@limiter.limit("20/minute")
async def upload(
    request: Request,
    file: UploadFile = File(...),
    task_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles([
            "admin",
            "manager",
            "employee",
        ])
    ),
):
    return await upload_document_service(
        db,
        file,
        user,
        task_id,
    )


@router.get(
    "/task/{task_id}",
    response_model=Page[DocumentOut],
)
@limiter.limit("60/minute")
def task_documents(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_task_documents_service(
        db,
        task_id,
        user,
    )


@router.get("/{document_id}")
@limiter.limit("30/minute")
def download(
    request: Request,
    document_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    doc = get_document_service(
        db,
        document_id,
        user,
    )

    return FileResponse(
        path=doc.file_path,
        filename=doc.file_name,
        media_type="application/octet-stream",
    )