from typing import Any
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
)

from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class NotificationPreference(Base):
    __tablename__ = (
        "notification_preferences"
    )

    id: Mapped[Any] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    in_app_enabled: Mapped[Any] = mapped_column(
        Boolean,
        default=True,
    )

    email_enabled: Mapped[Any] = mapped_column(
        Boolean,
        default=True,
    )

    task_notifications: Mapped[Any] = mapped_column(
        Boolean,
        default=True,
    )

    approval_notifications: Mapped[Any] = mapped_column(
        Boolean,
        default=True,
    )

    escalation_notifications: Mapped[Any] = mapped_column(
        Boolean,
        default=True,
    )

    document_notifications: Mapped[Any] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )