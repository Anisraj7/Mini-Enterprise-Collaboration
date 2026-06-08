from typing import Any
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[Any] = mapped_column(String(100), nullable=False)

    email: Mapped[Any] = mapped_column(String(255), unique=True, nullable=False, index=True)

    hashed_password: Mapped[Any] = mapped_column(String(255), nullable=False)

    role: Mapped[Any] = mapped_column(String(30), default="employee", nullable=False, index=True)
    
    is_active: Mapped[Any] = mapped_column(Boolean, default=True, index=True)

    created_at: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow)

    updated_at: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization_id: Mapped[Any] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=True, index=True
    )

    organization = relationship("Organization", back_populates="users")

    __table_args__ = (
        Index("idx_user_role_active", "role", "is_active"),
        Index("idx_user_org_role", "organization_id", "role"),
    )
