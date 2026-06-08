import os
import shutil

from pathlib import Path

from fastapi import (
    HTTPException,
    UploadFile,
    status,
)

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.cache import (
    cache_get,
    cache_set,
    invalidate_read_caches,
)

from app.models.document import Document

from app.services.notification_service import (
    create_notification,
)
from app.services.event_log_service import record_event

from app.repository.document_repository import (
    get_document_by_id,
    get_task_by_id,
    documents_query,
    get_existing_document,
    create_document_repository,
    commit_refresh,
)

UPLOAD_DIR = "uploads"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".txt",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


def can_access_document(
    user,
    document,
    task,
):

    if user.role in (
        "super_admin",
        "organization_admin",
        "workspace_admin",
    ):
        return True

    if not task:
        return document.uploaded_by == user.id

    if user.role == "manager":
        return (
            task.created_by_id == user.id
            or task.assigned_to_id == user.id
            or document.uploaded_by == user.id
        )

    return (
        task.assigned_to_id == user.id
        or document.uploaded_by == user.id
    )


def validate_task_access(
    task,
    user,
):

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if (
        user.organization_id
        and task.organization_id != user.organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if (
        user.role not in (
            "super_admin",
            "organization_admin",
            "workspace_admin",
        )
        and task.created_by_id != user.id
        and task.assigned_to_id != user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


def validate_file(
    file,
):

    suffix = Path(
        file.filename or ""
    ).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type",
        )


async def upload_document_service(
    db: Session,
    file: UploadFile,
    user,
    task_id: int,
):

    task = get_task_by_id(
        db,
        task_id,
    )

    validate_task_access(
        task,
        user,
    )

    validate_file(file)

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large",
        )

    await file.seek(0)

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True,
    )

    safe_name = Path(
        file.filename or ""
    ).name

    existing = get_existing_document(
        db,
        safe_name,
        task_id,
    )

    version = 1

    if existing:
        version = existing.version + 1

    file_path = (
        f"{UPLOAD_DIR}/"
        f"{task_id}_{version}_{safe_name}"
    )

    with open(file_path, "wb") as f:
        shutil.copyfileobj(
            file.file,
            f,
        )

    document = Document(
        file_name=safe_name,
        file_path=file_path,
        version=version,
        uploaded_by=user.id,
        task_id=task_id,
        organization_id=user.organization_id,
    )

    create_document_repository(
        db,
        document,
    )

    record_event(
        db,
        user_id=user.id,
        action="DOCUMENT_UPLOADED",
        entity_type="DOCUMENT",
        entity_id=document.id,
        organization_id=user.organization_id,
    )

    if (
        task.assigned_to_id
        and task.assigned_to_id != user.id
    ):
        create_notification(
            db,
            task.assigned_to_id,
            f"New document uploaded: {task.title}",
            user.organization_id,
        )

    commit_refresh(
        db,
        document,
    )

    invalidate_read_caches()

    return document


def get_document_service(
    db: Session,
    document_id: int,
    user,
):

    document = get_document_by_id(
        db,
        document_id,
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    task = get_task_by_id(
        db,
        document.task_id,
    )

    if not can_access_document(
        user,
        document,
        task,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    if not os.path.exists(document.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File missing",
        )

    return document


def get_task_documents_service(
    db: Session,
    task_id: int,
    user,
):

    cache_key = (
        f"documents:task:"
        f"user:{user.id}:"
        f"role:{user.role}:"
        f"task:{task_id}"
    )

    cached = cache_get(cache_key)

    if cached:
        return cached

    task = get_task_by_id(
        db,
        task_id,
    )

    validate_task_access(
        task,
        user,
    )

    query = documents_query(
        db,
        task_id,
    )

    result = paginate(db, query)

    result = jsonable_encoder(result)

    cache_set(
        cache_key,
        result,
    )

    return result
