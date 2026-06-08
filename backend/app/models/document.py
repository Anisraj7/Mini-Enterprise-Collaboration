from typing import Any
from sqlalchemy import Integer, String, DateTime, ForeignKey, Index
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True, index=True)
    file_name: Mapped[Any] = mapped_column(String)
    file_path: Mapped[Any] = mapped_column(String)
    version: Mapped[Any] = mapped_column(Integer, default=1)
    uploaded_by: Mapped[Any] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    task_id: Mapped[Any] = mapped_column(Integer, ForeignKey("tasks.id"), index=True)
    created_at: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    organization_id: Mapped[Any] = mapped_column(Integer, ForeignKey("organizations.id"))

    __table_args__ = (
        Index('idx_document_task_id_version', 'task_id', 'version'),
        Index('idx_document_uploaded_by_created_at', 'uploaded_by', 'created_at'),
    )