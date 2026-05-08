import os
import shutil
from pathlib import Path
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.task import Task

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx", ".xls", ".xlsx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024

def can_access_document(user, document: Document, db: Session) -> bool:
    if user.role == "admin":
        return True
    task = db.query(Task).filter(Task.id == document.task_id).first()
    if not task:
        return document.uploaded_by == user.id
    if user.role == "manager":
        return task.created_by_id == user.id or task.assigned_to_id == user.id or document.uploaded_by == user.id
    return task.assigned_to_id == user.id or document.uploaded_by == user.id

def _get_task_or_403(db: Session, task_id: int, user):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if user.role != "admin" and task.created_by_id != user.id and task.assigned_to_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return task

def _validate_file(file):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")

def upload_document(db: Session, file, user, task_id: int):
    _get_task_or_403(db, task_id, user)
    _validate_file(file)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    existing = db.query(Document).filter(
        Document.file_name == file.filename,
        Document.task_id == task_id
    ).order_by(Document.version.desc()).first()

    version = 1
    if existing:
        version = existing.version + 1

    safe_name = Path(file.filename).name
    file_path = f"{UPLOAD_DIR}/{task_id}_{version}_{safe_name}"

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        os.remove(file_path)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")

    doc = Document(
        file_name=safe_name,
        file_path=file_path,
        version=version,
        uploaded_by=user.id,
        task_id=task_id
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    return doc

def get_document(db: Session, document_id: int, user):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if not can_access_document(user, doc, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return doc

def get_task_documents(db: Session, task_id: int, user):
    _get_task_or_403(db, task_id, user)
    return (
        db.query(Document)
        .filter(Document.task_id == task_id)
        .order_by(Document.created_at.desc())
        .all()
    )
