from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)

from app.db.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=True,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
        default="System Notification",
    )

    message = Column(
        Text,
        nullable=False,
        default="",
    )

    notification_type = Column(
        String(100),
        nullable=False,
        default="GENERAL",
        index=True,
    )

    priority = Column(
        String(50),
        nullable=False,
        default="MEDIUM",
        index=True,
    )

    is_read = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    __table_args__ = (
        Index(
            "idx_notification_user_id_is_read",
            "user_id",
            "is_read",
        ),
        Index(
            "idx_notification_user_id_created_at",
            "user_id",
            "created_at",
        ),
    )