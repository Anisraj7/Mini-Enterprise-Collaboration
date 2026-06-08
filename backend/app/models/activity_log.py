from typing import Any
from sqlalchemy import DateTime, ForeignKey, Integer, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.database import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Any] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action: Mapped[Any] = mapped_column(String, nullable=False, index=True)
    entity_type: Mapped[Any] = mapped_column(String, nullable=False, index=True)
    entity_id: Mapped[Any] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    organization_id: Mapped[Any] = mapped_column(Integer, ForeignKey("organizations.id"))

    user = relationship("User")

    __table_args__ = (
        Index('idx_activity_entity_type_entity_id', 'entity_type', 'entity_id'),
        Index('idx_activity_user_id_created_at', 'user_id', 'created_at'),
    )
