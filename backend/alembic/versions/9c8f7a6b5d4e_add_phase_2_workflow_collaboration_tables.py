"""add phase 2 workflow collaboration tables

Revision ID: 9c8f7a6b5d4e
Revises: ff98044ef74c
Create Date: 2026-04-29 19:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9c8f7a6b5d4e"
down_revision: Union[str, Sequence[str], None] = "ff98044ef74c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_table(table_name: str) -> bool:
    return sa.inspect(op.get_bind()).has_table(table_name)


def upgrade() -> None:
    if not _has_table("comments"):
        op.create_table(
            "comments",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("task_id", sa.Integer(), nullable=True),
            sa.Column("user_id", sa.Integer(), nullable=True),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("is_internal", sa.Boolean(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
    if not _has_table("approvals"):
        op.create_table(
            "approvals",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("title", sa.String(), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("requested_by", sa.Integer(), nullable=False),
            sa.Column("status", sa.String(), nullable=False),
            sa.Column("current_level", sa.String(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["requested_by"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_approvals_id"), "approvals", ["id"], unique=False)
    if not _has_table("approval_history"):
        op.create_table(
            "approval_history",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("approval_id", sa.Integer(), nullable=False),
            sa.Column("action_by", sa.Integer(), nullable=False),
            sa.Column("action", sa.String(), nullable=False),
            sa.Column("comment", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["action_by"], ["users.id"]),
            sa.ForeignKeyConstraint(["approval_id"], ["approvals.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_approval_history_id"), "approval_history", ["id"], unique=False)
    if not _has_table("activity_logs"):
        op.create_table(
            "activity_logs",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("action", sa.String(), nullable=False),
            sa.Column("entity_type", sa.String(), nullable=False),
            sa.Column("entity_id", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_activity_logs_id"), "activity_logs", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_activity_logs_id"), table_name="activity_logs")
    op.drop_table("activity_logs")
    op.drop_index(op.f("ix_approval_history_id"), table_name="approval_history")
    op.drop_table("approval_history")
    op.drop_index(op.f("ix_approvals_id"), table_name="approvals")
    op.drop_table("approvals")
    op.drop_table("comments")
