from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from app.services.document_service import upload_document
from app.db.database import get_db

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
def upload(file: UploadFile, task_id: int, db: Session = Depends(get_db)):
    user_id = 1  # replace with auth user
    return upload_document(db, file, user_id, task_id)