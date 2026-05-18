from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from datetime import datetime
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    file_path = Column(String)
    version = Column(Integer, default=1)
    uploaded_by = Column(Integer, ForeignKey("users.id"), index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    __table_args__ = (
        Index('idx_document_task_id_version', 'task_id', 'version'),
        Index('idx_document_uploaded_by_created_at', 'uploaded_by', 'created_at'),
    )