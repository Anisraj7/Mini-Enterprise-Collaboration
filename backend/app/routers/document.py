from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.models.audit import AuditLog
from app.schemas.document import DocumentOut
from app.services.document_service import get_document, get_task_documents, upload_document
from app.db.database import get_db
import os

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentOut)
def upload(file: UploadFile, task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    doc = upload_document(db, file, user, task_id)
    db.add(AuditLog(user_id=user.id, action="DOCUMENT_UPLOADED", entity="DOCUMENT", entity_id=doc.id))
    db.commit()
    db.refresh(doc)
    return doc

@router.get("/task/{task_id}", response_model=list[DocumentOut])
def task_documents(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_task_documents(db, task_id, user)

@router.get("/{document_id}")
def download(document_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    doc = get_document(db, document_id, user)
    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File missing")
    return FileResponse(doc.file_path, filename=doc.file_name)
