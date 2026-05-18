from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String, default="pending", nullable=False, index=True)
    current_level = Column(String, default="manager", nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    requester = relationship("User")

    __table_args__ = (
        Index('idx_approval_status_current_level', 'status', 'current_level'),
        Index('idx_approval_requested_by_status', 'requested_by', 'status'),
    )

    @property
    def requested_by_name(self):
        return self.requester.name if self.requester else None


class ApprovalHistory(Base):
    __tablename__ = "approval_history"

    id = Column(Integer, primary_key=True, index=True)
    approval_id = Column(Integer, ForeignKey("approvals.id"), nullable=False, index=True)
    action_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    approval = relationship("Approval")
    user = relationship("User")
    
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    __table_args__ = (
        Index('idx_approval_history_approval_id_created_at', 'approval_id', 'created_at'),
    )

    @property
    def action_by_name(self):
        return self.user.name if self.user else None
