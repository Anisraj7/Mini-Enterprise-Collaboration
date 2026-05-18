from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Index
from datetime import datetime
from app.db.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    action = Column(String, index=True)
    entity = Column(String, index=True)
    entity_id = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    __table_args__ = (
        Index('idx_audit_entity_entity_id', 'entity', 'entity_id'),
        Index('idx_audit_user_id_timestamp', 'user_id', 'timestamp'),
    )
