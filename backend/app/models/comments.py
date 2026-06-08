from typing import Any
from sqlalchemy import Integer, Text, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[Any] = mapped_column(Integer, ForeignKey("tasks.id"), index=True)
    user_id: Mapped[Any] = mapped_column(Integer, ForeignKey("users.id"), index=True)

    content: Mapped[Any] = mapped_column(Text, nullable=False)
    is_internal: Mapped[Any] = mapped_column(Boolean, default=False)

    created_at: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User")
    
    organization_id: Mapped[Any] = mapped_column(Integer, ForeignKey("organizations.id"))

    __table_args__ = (
        Index('idx_comment_task_id_created_at', 'task_id', 'created_at'),
        Index('idx_comment_user_id_created_at', 'user_id', 'created_at'),
    )

    @property
    def user_name(self):
        return self.user.name if self.user else None
