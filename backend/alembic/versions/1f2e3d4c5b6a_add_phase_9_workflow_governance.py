"""add phase 9 workflow governance

Revision ID: 1f2e3d4c5b6a
Revises: ff98812a0179
Create Date: 2026-05-26 20:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1f2e3d4c5b6a"
down_revision: Union[str, Sequence[str], None] = "ff98812a0179"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sla_rules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("module_name", sa.String(length=100), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("allowed_hours", sa.Integer(), nullable=False),
        sa.Column("escalation_enabled", sa.Boolean(), nullable=True),
        sa.Column("escalation_after_hours", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sla_rules_id"), "sla_rules", ["id"], unique=False)

    op.create_table(
        "sla_tracking",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("module_name", sa.String(length=100), nullable=False),
        sa.Column("record_id", sa.Integer(), nullable=False),
        sa.Column("sla_rule_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("due_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=True),
        sa.Column("breach_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["sla_rule_id"], ["sla_rules.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sla_tracking_id"), "sla_tracking", ["id"], unique=False)

    op.create_table(
        "approval_escalations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("approval_id", sa.Integer(), nullable=False),
        sa.Column("escalated_from", sa.Integer(), nullable=False),
        sa.Column("escalated_to", sa.Integer(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("escalation_level", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("escalated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["approval_id"], ["approvals.id"]),
        sa.ForeignKeyConstraint(["escalated_from"], ["users.id"]),
        sa.ForeignKeyConstraint(["escalated_to"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_approval_escalations_id"), "approval_escalations", ["id"], unique=False)

    op.create_table(
        "approval_delegations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("delegator_id", sa.Integer(), nullable=False),
        sa.Column("delegatee_id", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("end_date", sa.DateTime(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["delegatee_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["delegator_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_approval_delegations_id"), "approval_delegations", ["id"], unique=False)
    op.create_index(op.f("ix_approval_delegations_delegator_id"), "approval_delegations", ["delegator_id"], unique=False)
    op.create_index(op.f("ix_approval_delegations_delegatee_id"), "approval_delegations", ["delegatee_id"], unique=False)
    op.create_index(op.f("ix_approval_delegations_start_date"), "approval_delegations", ["start_date"], unique=False)
    op.create_index(op.f("ix_approval_delegations_end_date"), "approval_delegations", ["end_date"], unique=False)
    op.create_index(op.f("ix_approval_delegations_is_active"), "approval_delegations", ["is_active"], unique=False)

    op.create_table(
        "notification_preferences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("in_app_enabled", sa.Boolean(), nullable=True),
        sa.Column("email_enabled", sa.Boolean(), nullable=True),
        sa.Column("task_notifications", sa.Boolean(), nullable=True),
        sa.Column("approval_notifications", sa.Boolean(), nullable=True),
        sa.Column("escalation_notifications", sa.Boolean(), nullable=True),
        sa.Column("document_notifications", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(op.f("ix_notification_preferences_id"), "notification_preferences", ["id"], unique=False)

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(sa.Column("sla_status", sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column("sla_due_time", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("is_sla_breached", sa.Boolean(), nullable=False, server_default=sa.text("0")))
        batch_op.create_index("ix_tasks_sla_status", ["sla_status"])
        batch_op.create_index("ix_tasks_sla_due_time", ["sla_due_time"])
        batch_op.create_index("ix_tasks_is_sla_breached", ["is_sla_breached"])

    with op.batch_alter_table("notifications") as batch_op:
        batch_op.add_column(sa.Column("title", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("notification_type", sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column("priority", sa.String(length=50), nullable=True))
        batch_op.create_index("ix_notifications_notification_type", ["notification_type"])
        batch_op.create_index("ix_notifications_priority", ["priority"])

    with op.batch_alter_table("approvals") as batch_op:
        batch_op.add_column(sa.Column("sla_status", sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column("sla_due_time", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("is_escalated", sa.Boolean(), nullable=False, server_default=sa.text("0")))
        batch_op.add_column(sa.Column("current_escalation_to", sa.Integer(), nullable=True))
        batch_op.create_foreign_key("fk_approvals_current_escalation_to_users", "users", ["current_escalation_to"], ["id"])
        batch_op.create_index("ix_approvals_sla_status", ["sla_status"])
        batch_op.create_index("ix_approvals_sla_due_time", ["sla_due_time"])
        batch_op.create_index("ix_approvals_is_escalated", ["is_escalated"])
        batch_op.create_index("ix_approvals_current_escalation_to", ["current_escalation_to"])

    with op.batch_alter_table("audit_logs") as batch_op:
        batch_op.add_column(sa.Column("organization_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("module_name", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("action_type", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("record_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("old_data", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("new_data", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("ip_address", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("user_agent", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), nullable=True))
        batch_op.create_index("idx_audit_module_record", ["module_name", "record_id"])
        batch_op.create_index("idx_audit_user_created", ["user_id", "created_at"])
        batch_op.create_index("idx_audit_org_created", ["organization_id", "created_at"])


def downgrade() -> None:
    with op.batch_alter_table("approvals") as batch_op:
        batch_op.drop_index("ix_approvals_current_escalation_to")
        batch_op.drop_index("ix_approvals_is_escalated")
        batch_op.drop_index("ix_approvals_sla_due_time")
        batch_op.drop_index("ix_approvals_sla_status")
        batch_op.drop_constraint("fk_approvals_current_escalation_to_users", type_="foreignkey")
        batch_op.drop_column("current_escalation_to")
        batch_op.drop_column("is_escalated")
        batch_op.drop_column("sla_due_time")
        batch_op.drop_column("sla_status")

    with op.batch_alter_table("notifications") as batch_op:
        batch_op.drop_index("ix_notifications_priority")
        batch_op.drop_index("ix_notifications_notification_type")
        batch_op.drop_column("priority")
        batch_op.drop_column("notification_type")
        batch_op.drop_column("title")

    with op.batch_alter_table("audit_logs") as batch_op:
        batch_op.drop_index("idx_audit_org_created")
        batch_op.drop_index("idx_audit_user_created")
        batch_op.drop_index("idx_audit_module_record")
        batch_op.drop_column("created_at")
        batch_op.drop_column("user_agent")
        batch_op.drop_column("ip_address")
        batch_op.drop_column("new_data")
        batch_op.drop_column("old_data")
        batch_op.drop_column("record_id")
        batch_op.drop_column("action_type")
        batch_op.drop_column("module_name")
        batch_op.drop_column("organization_id")

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_index("ix_tasks_is_sla_breached")
        batch_op.drop_index("ix_tasks_sla_due_time")
        batch_op.drop_index("ix_tasks_sla_status")
        batch_op.drop_column("is_sla_breached")
        batch_op.drop_column("sla_due_time")
        batch_op.drop_column("sla_status")

    op.drop_index(op.f("ix_notification_preferences_id"), table_name="notification_preferences")
    op.drop_table("notification_preferences")
    op.drop_index(op.f("ix_approval_delegations_is_active"), table_name="approval_delegations")
    op.drop_index(op.f("ix_approval_delegations_end_date"), table_name="approval_delegations")
    op.drop_index(op.f("ix_approval_delegations_start_date"), table_name="approval_delegations")
    op.drop_index(op.f("ix_approval_delegations_delegatee_id"), table_name="approval_delegations")
    op.drop_index(op.f("ix_approval_delegations_delegator_id"), table_name="approval_delegations")
    op.drop_index(op.f("ix_approval_delegations_id"), table_name="approval_delegations")
    op.drop_table("approval_delegations")
    op.drop_index(op.f("ix_approval_escalations_id"), table_name="approval_escalations")
    op.drop_table("approval_escalations")
    op.drop_index(op.f("ix_sla_tracking_id"), table_name="sla_tracking")
    op.drop_table("sla_tracking")
    op.drop_index(op.f("ix_sla_rules_id"), table_name="sla_rules")
    op.drop_table("sla_rules")
