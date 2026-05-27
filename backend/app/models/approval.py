from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Index,
)
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
    sla_status = Column(String(50), nullable=True, index=True)
    sla_due_time = Column(DateTime, nullable=True, index=True)
    is_escalated = Column(Boolean, default=False, nullable=False, index=True)
    current_escalation_to = Column(
        Integer, ForeignKey("users.id"), nullable=True, index=True
    )

    organization_id = Column(Integer, ForeignKey("organizations.id"))

    requester = relationship("User", foreign_keys=[requested_by])
    escalation_user = relationship("User", foreign_keys=[current_escalation_to])

    escalations = relationship(
        "ApprovalEscalation",
        back_populates="approval",
        cascade="all, delete-orphan",
    )
    __table_args__ = (
        Index("idx_approval_status_current_level", "status", "current_level"),
        Index("idx_approval_requested_by_status", "requested_by", "status"),
    )

    @property
    def requested_by_name(self):
        return self.requester.name if self.requester else None


class ApprovalHistory(Base):
    __tablename__ = "approval_history"

    id = Column(Integer, primary_key=True, index=True)
    approval_id = Column(
        Integer, ForeignKey("approvals.id"), nullable=False, index=True
    )
    action_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    approval = relationship("Approval")
    user = relationship("User")

    organization_id = Column(Integer, ForeignKey("organizations.id"))

    __table_args__ = (
        Index(
            "idx_approval_history_approval_id_created_at", "approval_id", "created_at"
        ),
    )

    @property
    def action_by_name(self):
        return self.user.name if self.user else None
    
    
    @property
    def current_escalation_to_name(
        self,
    ):
        return (
            self.escalation_user.name
            if self.escalation_user
            else None
        )