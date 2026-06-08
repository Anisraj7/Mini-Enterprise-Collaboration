from typing import Any
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class SLARule(Base):
    __tablename__ = "sla_rules"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True, index=True)

    module_name: Mapped[Any] = mapped_column(String(100), nullable=False)

    priority: Mapped[Any] = mapped_column(String(50), nullable=False)

    allowed_hours: Mapped[Any] = mapped_column(Integer, nullable=False)

    escalation_enabled: Mapped[Any] = mapped_column(
        Boolean,
        default=False,
    )

    escalation_after_hours: Mapped[Any] = mapped_column(
        Integer,
        nullable=True,
    )

    is_active: Mapped[Any] = mapped_column(
        Boolean,
        default=True,
    )

    created_by: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )