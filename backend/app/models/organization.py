from typing import Any
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Index,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    synonym,
)

from app.db.database import Base


class Organization(Base):
    """
    Organization model.

    Represents a SaaS tenant in the system.
    Each organization owns its users, workspaces,
    channels, settings, and collaboration data.
    """

    __tablename__ = "organizations"

    id: Mapped[Any] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[Any] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    contact_email: Mapped[Any] = mapped_column(
        "email",
        String(255),
        nullable=False,
        unique=True
    )

    email = synonym("contact_email")

    slug: Mapped[Any] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
        index=True
    )

    phone: Mapped[Any] = mapped_column(
        String(50),
        nullable=True
    )

    address: Mapped[Any] = mapped_column(
        String(255),
        nullable=True
    )

    industry: Mapped[Any] = mapped_column(
        String(120),
        nullable=True
    )

    plan: Mapped[Any] = mapped_column(
        String(50),
        nullable=False,
        default="basic"
    )

    status: Mapped[Any] = mapped_column(
        String(50),
        nullable=False,
        default="ACTIVE"
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

    users = relationship(
        "User",
        back_populates="organization"
    )

    onboarding_records = relationship(
        "TenantOnboarding",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    collaboration_settings = relationship(
        "TenantCollaborationSettings",
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan"
    )

    collaboration_usage = relationship(
        "TenantCollaborationUsage",
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan"
    )

    workspaces = relationship(
        "Workspace",
        back_populates="organization"
    )

    channels = relationship(
        "Channel",
        back_populates="organization"
    )

    __table_args__ = (
        Index(
            "idx_organization_status",
            "status"
        ),
    )