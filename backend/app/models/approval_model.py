from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    BigInteger,
    Index,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base


class ApprovalDocument(Base):
    __tablename__ = "approval_documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    organization_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    approval_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "approvals.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    uploaded_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    document_type: Mapped[str] = mapped_column(
        String(50),
        default="OTHER",
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    # Relationships

    approval = relationship(
        "Approval",
        passive_deletes=True,
    )

    uploader = relationship(
        "User",
        foreign_keys=[uploaded_by],
    )

    organization = relationship(
        "Organization",
    )

    __table_args__ = (
        Index(
            "idx_approval_document_approval_created",
            "approval_id",
            "created_at",
        ),
        Index(
            "idx_approval_document_org_approval",
            "organization_id",
            "approval_id",
        ),
    )