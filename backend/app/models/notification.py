from typing import Any
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id: Mapped[Any] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    organization_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=True,
        index=True,
    )

    title: Mapped[Any] = mapped_column(
        String(255),
        nullable=False,
        default="System Notification",
    )

    message: Mapped[Any] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    notification_type: Mapped[Any] = mapped_column(
        String(100),
        nullable=False,
        default="GENERAL",
        index=True,
    )

    priority: Mapped[Any] = mapped_column(
        String(50),
        nullable=False,
        default="MEDIUM",
        index=True,
    )

    is_read: Mapped[Any] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
    )

    created_at: Mapped[Any] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    __table_args__ = (
        Index(
            "idx_notification_user_id_is_read",
            "user_id",
            "is_read",
        ),
        Index(
            "idx_notification_user_id_created_at",
            "user_id",
            "created_at",
        ),
    )