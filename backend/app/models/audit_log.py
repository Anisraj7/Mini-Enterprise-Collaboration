from typing import Any
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[Any] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    organization_id: Mapped[Any] = mapped_column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=True,
        index=True,
    )

    # =====================================
    # MODULE / ENTITY INFO
    # =====================================
    module_name: Mapped[Any] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    action_type: Mapped[Any] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    record_id: Mapped[Any] = mapped_column(
        Integer,
        nullable=True,
        index=True,
    )

    # =====================================
    # DATA SNAPSHOTS
    # =====================================
    old_data: Mapped[Any] = mapped_column(
        Text,
        nullable=True,
    )

    new_data: Mapped[Any] = mapped_column(
        Text,
        nullable=True,
    )

    # =====================================
    # REQUEST INFO
    # =====================================
    ip_address: Mapped[Any] = mapped_column(
        String,
        nullable=True,
    )

    user_agent: Mapped[Any] = mapped_column(
        Text,
        nullable=True,
    )

    # =====================================
    # TIMESTAMP
    # =====================================
    created_at: Mapped[Any] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )

    __table_args__ = (

        # entity lookup
        Index(
            "idx_audit_module_record",
            "module_name",
            "record_id",
        ),

        # user activity timeline
        Index(
            "idx_audit_user_created",
            "user_id",
            "created_at",
        ),

        # organization filtering
        Index(
            "idx_audit_org_created",
            "organization_id",
            "created_at",
        ),
    )