from typing import Any
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class SLATracking(Base):
    __tablename__ = "sla_tracking"

    id: Mapped[Any] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    module_name: Mapped[Any] = mapped_column(
        String(100),
        nullable=False,
    )

    record_id: Mapped[Any] = mapped_column(
        Integer,
        nullable=False,
    )

    sla_rule_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("sla_rules.id"),
        nullable=False,
    )

    start_time: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    due_time: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    completed_time: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    status: Mapped[Any] = mapped_column(
        String(100),
        default="ACTIVE",
    )

    breach_reason: Mapped[Any] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )