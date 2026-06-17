from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        Enum(
            "todo",
            "in_progress",
            "review",
            "done",
            name="task_status",
        ),
        default="todo",
        nullable=False,
        index=True,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="medium",
        nullable=False,
        index=True,
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )

    created_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    assigned_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True,
    )

    channel_id: Mapped[int | None] = mapped_column(
        ForeignKey("channels.id"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        index=True,
    )

    document: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    sla_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )

    sla_due_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )

    is_sla_breached: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    # Relationships

    created_by = relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    assigned_to = relationship(
        "User",
        foreign_keys=[assigned_to_id],
    )

    updated_by_user = relationship(
        "User",
        foreign_keys=[updated_by],
    )

    organization = relationship(
        "Organization",
    )

    workspace = relationship(
        "Workspace",
    )

    channel = relationship(
        "Channel",
    )

    __table_args__ = (
        Index(
            "idx_task_status_updated_at",
            "status",
            "updated_at",
        ),
        Index(
            "idx_task_assigned_to_status",
            "assigned_to_id",
            "status",
        ),
        Index(
            "idx_task_created_by_status",
            "created_by_id",
            "status",
        ),
        Index(
            "idx_task_due_date",
            "due_date",
        ),
    )

    @property
    def assigned_to_name(self) -> str | None:
        return (
            self.assigned_to.name
            if self.assigned_to
            else None
        )


class TaskHistory(Base):
    __tablename__ = "task_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False,
        index=True,
    )

    old_status: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    new_status: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    changed_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    task = relationship(
        "Task",
    )

    user = relationship(
        "User",
    )

    __table_args__ = (
        Index(
            "idx_task_history_task_id_changed_at",
            "task_id",
            "changed_at",
        ),
    )