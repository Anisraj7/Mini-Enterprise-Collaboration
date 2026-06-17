from typing import Any
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.database import Base


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[Any] = mapped_column(String, nullable=False)
    description: Mapped[Any] = mapped_column(Text)
    requested_by: Mapped[Any] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status: Mapped[Any] = mapped_column(String, default="pending", nullable=False, index=True)
    current_level: Mapped[Any] = mapped_column(String, default="manager", nullable=False, index=True)
    created_at: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    sla_status: Mapped[Any] = mapped_column(String(50), nullable=True, index=True)
    sla_due_time: Mapped[Any] = mapped_column(DateTime, nullable=True, index=True)
    is_escalated: Mapped[Any] = mapped_column(Boolean, default=False, nullable=False, index=True)
    current_escalation_to: Mapped[Any] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True, index=True
    )

    organization_id: Mapped[Any] = mapped_column(Integer, ForeignKey("organizations.id"))

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
    
    documents = relationship(
        "ApprovalDocument",
        back_populates="approval",
        cascade="all, delete-orphan",
        )

    @property
    def requested_by_name(self):
        return self.requester.name if self.requester else None


class ApprovalHistory(Base):
    __tablename__ = "approval_history"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True, index=True)
    approval_id: Mapped[Any] = mapped_column(
        Integer, ForeignKey("approvals.id"), nullable=False, index=True
    )
    action_by: Mapped[Any] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action: Mapped[Any] = mapped_column(String, nullable=False)
    comment: Mapped[Any] = mapped_column(Text)
    created_at: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    approval = relationship("Approval")
    user = relationship("User")

    organization_id: Mapped[Any] = mapped_column(Integer, ForeignKey("organizations.id"))

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
        
    