from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.sql import func

from app.db.database import Base


class SLATracking(Base):
    __tablename__ = "sla_tracking"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    module_name = Column(
        String(100),
        nullable=False,
    )

    record_id = Column(
        Integer,
        nullable=False,
    )

    sla_rule_id = Column(
        Integer,
        ForeignKey("sla_rules.id"),
        nullable=False,
    )

    start_time = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    due_time = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    completed_time = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    status = Column(
        String(100),
        default="ACTIVE",
    )

    breach_reason = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )