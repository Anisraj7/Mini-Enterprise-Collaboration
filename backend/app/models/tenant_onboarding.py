from typing import Any
from datetime import datetime

from sqlalchemy import (
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Index,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class TenantOnboarding(Base):
    __tablename__ = "tenant_onboarding"

    id: Mapped[Any] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    admin_user_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    onboarding_status: Mapped[Any] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    default_workspace_created: Mapped[Any] = mapped_column(
        Boolean,
        default=False
    )

    settings_created: Mapped[Any] = mapped_column(
        Boolean,
        default=False
    )

    completed_at: Mapped[Any] = mapped_column(
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
        back_populates="onboarding_records"
    )

    admin_user = relationship(
        "User",
        foreign_keys=[admin_user_id]
    )

    __table_args__ = (
        Index(
            "idx_tenant_onboarding_status",
            "onboarding_status"
        ),
    )