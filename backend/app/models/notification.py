from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Index
from datetime import datetime
from app.db.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    message = Column(String)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    __table_args__ = (
        Index('idx_notification_user_id_is_read', 'user_id', 'is_read'),
        Index('idx_notification_user_id_created_at', 'user_id', 'created_at'),
    )
