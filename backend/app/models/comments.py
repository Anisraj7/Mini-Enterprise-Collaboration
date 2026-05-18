from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    content = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User")
    
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    __table_args__ = (
        Index('idx_comment_task_id_created_at', 'task_id', 'created_at'),
        Index('idx_comment_user_id_created_at', 'user_id', 'created_at'),
    )

    @property
    def user_name(self):
        return self.user.name if self.user else None
