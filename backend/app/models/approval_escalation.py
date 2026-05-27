from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class ApprovalEscalation(Base):

    __tablename__ = "approval_escalations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    approval_id = Column(
        Integer,
        ForeignKey("approvals.id"),
        nullable=False,
    )

    escalated_from = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    escalated_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    reason = Column(
        String(500),
        nullable=False,
    )

    escalation_level = Column(
        Integer,
        default=1,
    )

    status = Column(
        String(50),
        default="PENDING",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    resolved_at = Column(
        DateTime,
        nullable=True,
    )

    # =====================================
    # RELATIONSHIPS
    # =====================================

    approval = relationship(
        "Approval",
        back_populates="escalations",
        foreign_keys=[approval_id],
    )

    escalated_from_user = relationship(
        "User",
        foreign_keys=[escalated_from],
        lazy="joined",
    )

    escalated_to_user = relationship(
        "User",
        foreign_keys=[escalated_to],
        lazy="joined",
    )