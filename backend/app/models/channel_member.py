from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base




class ChannelMember(Base):
    __tablename__ = "channel_members"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    channel_id: Mapped[int] = mapped_column(
        ForeignKey(
            "channels.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    is_muted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_read_message_id: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )

    # Relationships

    channel: Mapped["Channel"] = relationship(
        back_populates="members",
        passive_deletes=True,
    )

    user: Mapped["User"] = relationship(
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "channel_id",
            "user_id",
            name="uq_channel_member",
        ),
        Index(
            "idx_channel_member_channel_user",
            "channel_id",
            "user_id",
        ),
        Index(
            "idx_channel_member_channel_joined",
            "channel_id",
            "joined_at",
        ),
    )