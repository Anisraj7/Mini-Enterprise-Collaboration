from typing import Any
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[Any] = mapped_column(String(200), nullable=False)

    description: Mapped[Any] = mapped_column(String(1000), nullable=True)

    status: Mapped[Any] = mapped_column(
        Enum("todo", "in_progress", "review", "done", name="task_status"),
        default="todo",
        nullable=False,
        index=True
    )

    priority: Mapped[Any] = mapped_column(String(20), default="medium", nullable=False, index=True)

    due_date: Mapped[Any] = mapped_column(DateTime, nullable=True, index=True)

    created_by_id: Mapped[Any] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    assigned_to_id: Mapped[Any] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    updated_by: Mapped[Any] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    organization_id: Mapped[Any] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=True, index=True)

    created_at: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    updated_at: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    document: Mapped[Any] = mapped_column(String, nullable=True)

    sla_status: Mapped[Any] = mapped_column(String(50), nullable=True, index=True)

    sla_due_time: Mapped[Any] = mapped_column(DateTime, nullable=True, index=True)

    is_sla_breached: Mapped[Any] = mapped_column(Boolean, default=False, nullable=False, index=True)

    created_by = relationship("User", foreign_keys=[created_by_id])

    assigned_to = relationship("User", foreign_keys=[assigned_to_id])

    updated_by_user = relationship("User", foreign_keys=[updated_by])

    __table_args__ = (
        Index("idx_task_status_updated_at", "status", "updated_at"),
        Index("idx_task_assigned_to_status", "assigned_to_id", "status"),
        Index("idx_task_created_by_status", "created_by_id", "status"),
        Index("idx_task_due_date", "due_date"),
    )

    @property
    def assigned_to_name(self):
        return self.assigned_to.name if self.assigned_to else None


class TaskHistory(Base):
    __tablename__ = "task_history"

    id: Mapped[Any] = mapped_column(Integer, primary_key=True, index=True)

    task_id: Mapped[Any] = mapped_column(Integer, ForeignKey("tasks.id"), nullable=False, index=True)

    old_status: Mapped[Any] = mapped_column(String, nullable=False)

    new_status: Mapped[Any] = mapped_column(String, nullable=False)

    changed_by: Mapped[Any] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    changed_at: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    task = relationship("Task")

    user = relationship("User")

    __table_args__ = (
        Index("idx_task_history_task_id_changed_at", "task_id", "changed_at"),
    )
