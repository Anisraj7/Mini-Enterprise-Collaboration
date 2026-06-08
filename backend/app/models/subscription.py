from typing import Any
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Subscription(Base):

    __tablename__ = "subscriptions"

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

    plan: Mapped[Any] = mapped_column(
        String(20),
        default="basic",
        nullable=False
    )

    credits: Mapped[Any] = mapped_column(
        Integer,
        default=100,
        nullable=False
    )

    status: Mapped[Any] = mapped_column(
        String(20),
        default="active",
        nullable=False
    )

    razorpay_order_id: Mapped[Any] = mapped_column(
        String(255),
        nullable=True,
        unique=True
    )

    razorpay_payment_id: Mapped[Any] = mapped_column(
        String(255),
        nullable=True,
        unique=True
    )

    stripe_session_id: Mapped[Any] = mapped_column(
        String(255),
        nullable=True,
        unique=True
    )

    stripe_payment_intent_id: Mapped[Any] = mapped_column(
        String(255),
        nullable=True,
        unique=True
    )

    start_date: Mapped[Any] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    end_date: Mapped[Any] = mapped_column(
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