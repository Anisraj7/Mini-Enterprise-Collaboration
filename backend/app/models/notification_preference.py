from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
)

from sqlalchemy.sql import func

from app.db.database import Base


class NotificationPreference(Base):
    __tablename__ = (
        "notification_preferences"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    in_app_enabled = Column(
        Boolean,
        default=True,
    )

    email_enabled = Column(
        Boolean,
        default=True,
    )

    task_notifications = Column(
        Boolean,
        default=True,
    )

    approval_notifications = Column(
        Boolean,
        default=True,
    )

    escalation_notifications = Column(
        Boolean,
        default=True,
    )

    document_notifications = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )