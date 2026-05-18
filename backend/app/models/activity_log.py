from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String, nullable=False, index=True)
    entity_type = Column(String, nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    user = relationship("User")

    __table_args__ = (
        Index('idx_activity_entity_type_entity_id', 'entity_type', 'entity_id'),
        Index('idx_activity_user_id_created_at', 'user_id', 'created_at'),
    )
