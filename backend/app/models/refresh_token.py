from typing import Any
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[Any] = mapped_column(Integer, ForeignKey("users.id"))

    token: Mapped[Any] = mapped_column(String, unique=True, nullable=False)

    expires_at: Mapped[Any] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )