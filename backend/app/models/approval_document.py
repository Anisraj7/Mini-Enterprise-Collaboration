from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum as SqlEnum,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base


class DocumentType(str, Enum):
    MEDICAL_CERTIFICATE = "MEDICAL_CERTIFICATE"
    INVOICE = "INVOICE"
    QUOTATION = "QUOTATION"
    LICENSE = "LICENSE"
    ESTIMATE = "ESTIMATE"
    OTHER = "OTHER"


class ApprovalDocument(Base):
    __tablename__ = "approval_documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    approval_id: Mapped[int] = mapped_column(
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
        Integer,
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    uploaded_by: Mapped[int | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    document_type: Mapped[DocumentType] = mapped_column(
        SqlEnum(
            DocumentType,
            name="approval_document_type",
        ),
        default=DocumentType.OTHER,
        nullable=False,
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
        back_populates="documents",
    )

    uploader = relationship(
        "User",
        foreign_keys=[uploaded_by],
    )

    organization = relationship(
        "Organization",
    )