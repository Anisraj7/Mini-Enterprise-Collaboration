from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)

from app.db.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=True,
        index=True,
    )

    # =====================================
    # MODULE / ENTITY INFO
    # =====================================
    module_name = Column(
        String,
        nullable=False,
        index=True,
    )

    action_type = Column(
        String,
        nullable=False,
        index=True,
    )

    record_id = Column(
        Integer,
        nullable=True,
        index=True,
    )

    # =====================================
    # DATA SNAPSHOTS
    # =====================================
    old_data = Column(
        Text,
        nullable=True,
    )

    new_data = Column(
        Text,
        nullable=True,
    )

    # =====================================
    # REQUEST INFO
    # =====================================
    ip_address = Column(
        String,
        nullable=True,
    )

    user_agent = Column(
        Text,
        nullable=True,
    )

    # =====================================
    # TIMESTAMP
    # =====================================
    created_at = Column(
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