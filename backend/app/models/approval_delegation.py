from typing import Any
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ApprovalDelegation(Base):
    __tablename__ = (
        "approval_delegations"
    )

    id: Mapped[Any] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    delegator_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    delegatee_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    start_date: Mapped[Any] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    end_date: Mapped[Any] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    reason: Mapped[Any] = mapped_column(
        Text,
        nullable=False,
    )

    is_active: Mapped[Any] = mapped_column(
        Boolean,
        default=True,
        index=True,
    )

    created_at: Mapped[Any] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )