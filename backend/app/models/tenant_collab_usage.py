from typing import Any
from datetime import datetime

from sqlalchemy import (
    Integer,
    DateTime,
    ForeignKey,
    Index,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class TenantCollaborationUsage(Base):
    __tablename__ = "tenant_collaboration_usage"

    id: Mapped[Any] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("organizations.id"),
        unique=True,
        nullable=False,
        index=True
    )

    workspace_count: Mapped[Any] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    channel_count: Mapped[Any] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    member_count: Mapped[Any] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    storage_used_mb: Mapped[Any] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    last_calculated_at: Mapped[Any] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[Any] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[Any] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    organization = relationship(
        "Organization",
        back_populates="collaboration_usage"
    )

    __table_args__ = (
        Index(
            "idx_tenant_collaboration_usage_org",
            "organization_id"
        ),
    )