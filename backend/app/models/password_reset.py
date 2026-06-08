from typing import Any
from datetime import datetime, timezone

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class PasswordResetToken(Base):

    __tablename__ = "password_reset_tokens"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("users.id")
    )

    token: Mapped[Any] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    expires_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True)
    )

    is_used: Mapped[Any] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )