from typing import Any
from datetime import datetime

from sqlalchemy import (
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class TenantCollaborationSettings(Base):
    __tablename__ = "tenant_collaboration_settings"

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

    max_workspaces: Mapped[Any] = mapped_column(
        Integer,
        nullable=False,
        default=10
    )

    max_channels_per_workspace: Mapped[Any] = mapped_column(
        Integer,
        nullable=False,
        default=50
    )

    max_workspace_members: Mapped[Any] = mapped_column(
        Integer,
        nullable=False,
        default=100
    )

    max_storage_mb: Mapped[Any] = mapped_column(
        Integer,
        nullable=False,
        default=1024
    )

    workspace_enabled: Mapped[Any] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    channel_enabled: Mapped[Any] = mapped_column(
        Boolean,
        nullable=False,
        default=True
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
        back_populates="collaboration_settings"
    )

    __table_args__ = (
        Index(
            "idx_tenant_collaboration_settings_org",
            "organization_id"
        ),
    )