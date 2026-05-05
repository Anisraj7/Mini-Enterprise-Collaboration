import os
from sqlalchemy.orm import Session
from app.models.document import Document

UPLOAD_DIR = "uploads"

def upload_document(db: Session, file, user_id: int, task_id: int):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    existing = db.query(Document).filter(
        Document.file_name == file.filename,
        Document.task_id == task_id
    ).order_by(Document.version.desc()).first()

    version = 1
    if existing:
        version = existing.version + 1

    file_path = f"{UPLOAD_DIR}/{version}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    doc = Document(
        file_name=file.filename,
        file_path=file_path,
        version=version,
        uploaded_by=user_id,
        task_id=task_id
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    return doc