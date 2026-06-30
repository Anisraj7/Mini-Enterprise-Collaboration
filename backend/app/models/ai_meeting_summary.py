from datetime import datetime

from sqlalchemy import (
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base


class AIMeetingSummary(Base):
    __tablename__ = "ai_meeting_summaries"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id"),
        nullable=False,
        unique=True,
        index=True
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    action_items: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    risks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    decisions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    meeting = relationship(
        "Meeting",
        back_populates="ai_summary"
    )