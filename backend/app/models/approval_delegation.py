from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)

from app.db.database import Base


class ApprovalDelegation(Base):
    __tablename__ = (
        "approval_delegations"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    delegator_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    delegatee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    start_date = Column(
        DateTime,
        nullable=False,
        index=True,
    )

    end_date = Column(
        DateTime,
        nullable=False,
        index=True,
    )

    reason = Column(
        Text,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        index=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )