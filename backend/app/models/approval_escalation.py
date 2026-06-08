from typing import Any
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ApprovalEscalation(Base):

    __tablename__ = "approval_escalations"

    id: Mapped[Any] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    approval_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("approvals.id"),
        nullable=False,
    )

    escalated_from: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    escalated_to: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    reason: Mapped[Any] = mapped_column(
        String(500),
        nullable=False,
    )

    escalation_level: Mapped[Any] = mapped_column(
        Integer,
        default=1,
    )

    status: Mapped[Any] = mapped_column(
        String(50),
        default="PENDING",
    )

    created_at: Mapped[Any] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    resolved_at: Mapped[Any] = mapped_column(
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