"""add phase 3 enterprise tables

Revision ID: 3b7c2d9e1f40
Revises: 9c8f7a6b5d4e
Create Date: 2026-05-07 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3b7c2d9e1f40"
down_revision: Union[str, Sequence[str], None] = "9c8f7a6b5d4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_table(table_name: str) -> bool:
    return sa.inspect(op.get_bind()).has_table(table_name)


def upgrade() -> None:
    if not _has_table("documents"):
        op.create_table(
            "documents",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("file_name", sa.String(), nullable=True),
            sa.Column("file_path", sa.String(), nullable=True),
            sa.Column("version", sa.Integer(), nullable=True),
            sa.Column("uploaded_by", sa.Integer(), nullable=True),
            sa.Column("task_id", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["uploaded_by"], ["users.id"]),
            sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_documents_id"), "documents", ["id"], unique=False)

    if not _has_table("audit_logs"):
        op.create_table(
            "audit_logs",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=True),
            sa.Column("action", sa.String(), nullable=True),
            sa.Column("entity", sa.String(), nullable=True),
            sa.Column("entity_id", sa.Integer(), nullable=True),
            sa.Column("timestamp", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )

    if not _has_table("notifications"):
        op.create_table(
            "notifications",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=True),
            sa.Column("message", sa.String(), nullable=True),
            sa.Column("is_read", sa.Boolean(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )


def downgrade() -> None:
    op.drop_table("notifications")
    op.drop_table("audit_logs")
    op.drop_index(op.f("ix_documents_id"), table_name="documents")
    op.drop_table("documents")
