"""Add database indexes for query optimization

Revision ID: db_query_optimization
Revises: 3b7c2d9e1f40
Create Date: 2026-05-13 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "db_query_optimization"
down_revision: Union[str, Sequence[str], None] = "3b7c2d9e1f40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # User table indexes
    op.create_index('idx_user_role_active', 'users', ['role', 'is_active'])
    op.create_index('idx_user_is_active', 'users', ['is_active'])
    op.create_index('idx_user_role', 'users', ['role'])

    # Task table indexes
    op.create_index('idx_task_status_updated_at', 'tasks', ['status', 'updated_at'])
    op.create_index('idx_task_assigned_to_status', 'tasks', ['assigned_to_id', 'status'])
    op.create_index('idx_task_created_by_status', 'tasks', ['created_by_id', 'status'])
    op.create_index('idx_task_created_by_id', 'tasks', ['created_by_id'])
    op.create_index('idx_task_assigned_to_id', 'tasks', ['assigned_to_id'])
    op.create_index('idx_task_status', 'tasks', ['status'])
    op.create_index('idx_task_priority', 'tasks', ['priority'])
    op.create_index('idx_task_created_at', 'tasks', ['created_at'])
    op.create_index('idx_task_updated_at', 'tasks', ['updated_at'])

    # TaskHistory table indexes
    op.create_index('idx_task_history_task_id_changed_at', 'task_history', ['task_id', 'changed_at'])
    op.create_index('idx_task_history_task_id', 'task_history', ['task_id'])
    op.create_index('idx_task_history_changed_by', 'task_history', ['changed_by'])
    op.create_index('idx_task_history_changed_at', 'task_history', ['changed_at'])

    # Document table indexes
    op.create_index('idx_document_task_id_version', 'documents', ['task_id', 'version'])
    op.create_index('idx_document_uploaded_by_created_at', 'documents', ['uploaded_by', 'created_at'])
    op.create_index('idx_document_task_id', 'documents', ['task_id'])
    op.create_index('idx_document_uploaded_by', 'documents', ['uploaded_by'])
    op.create_index('idx_document_created_at', 'documents', ['created_at'])

    # Notification table indexes
    op.create_index('idx_notification_user_id_is_read', 'notifications', ['user_id', 'is_read'])
    op.create_index('idx_notification_user_id_created_at', 'notifications', ['user_id', 'created_at'])
    op.create_index('idx_notification_user_id', 'notifications', ['user_id'])
    op.create_index('idx_notification_is_read', 'notifications', ['is_read'])
    op.create_index('idx_notification_created_at', 'notifications', ['created_at'])

    # Comment table indexes
    op.create_index('idx_comment_task_id_created_at', 'comments', ['task_id', 'created_at'])
    op.create_index('idx_comment_user_id_created_at', 'comments', ['user_id', 'created_at'])
    op.create_index('idx_comment_task_id', 'comments', ['task_id'])
    op.create_index('idx_comment_user_id', 'comments', ['user_id'])
    op.create_index('idx_comment_created_at', 'comments', ['created_at'])

    # AuditLog table indexes
    op.create_index('idx_audit_entity_entity_id', 'audit_logs', ['entity', 'entity_id'])
    op.create_index('idx_audit_user_id_timestamp', 'audit_logs', ['user_id', 'timestamp'])
    op.create_index('idx_audit_user_id', 'audit_logs', ['user_id'])
    op.create_index('idx_audit_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_entity', 'audit_logs', ['entity'])
    op.create_index('idx_audit_entity_id', 'audit_logs', ['entity_id'])
    op.create_index('idx_audit_timestamp', 'audit_logs', ['timestamp'])

    # ActivityLog table indexes
    op.create_index('idx_activity_entity_type_entity_id', 'activity_logs', ['entity_type', 'entity_id'])
    op.create_index('idx_activity_user_id_created_at', 'activity_logs', ['user_id', 'created_at'])
    op.create_index('idx_activity_user_id', 'activity_logs', ['user_id'])
    op.create_index('idx_activity_action', 'activity_logs', ['action'])
    op.create_index('idx_activity_entity_type', 'activity_logs', ['entity_type'])
    op.create_index('idx_activity_entity_id', 'activity_logs', ['entity_id'])

    # Approval table indexes
    op.create_index('idx_approval_status_current_level', 'approvals', ['status', 'current_level'])
    op.create_index('idx_approval_requested_by_status', 'approvals', ['requested_by', 'status'])
    op.create_index('idx_approval_requested_by', 'approvals', ['requested_by'])
    op.create_index('idx_approval_status', 'approvals', ['status'])
    op.create_index('idx_approval_current_level', 'approvals', ['current_level'])
    op.create_index('idx_approval_created_at', 'approvals', ['created_at'])

    # ApprovalHistory table indexes
    op.create_index('idx_approval_history_approval_id_created_at', 'approval_history', ['approval_id', 'created_at'])
    op.create_index('idx_approval_history_approval_id', 'approval_history', ['approval_id'])
    op.create_index('idx_approval_history_action_by', 'approval_history', ['action_by'])
    op.create_index('idx_approval_history_created_at', 'approval_history', ['created_at'])


def downgrade() -> None:
    # Drop all indexes in reverse order
    op.drop_index('idx_approval_history_created_at', table_name='approval_history')
    op.drop_index('idx_approval_history_action_by', table_name='approval_history')
    op.drop_index('idx_approval_history_approval_id', table_name='approval_history')
    op.drop_index('idx_approval_history_approval_id_created_at', table_name='approval_history')

    op.drop_index('idx_approval_created_at', table_name='approvals')
    op.drop_index('idx_approval_current_level', table_name='approvals')
    op.drop_index('idx_approval_status', table_name='approvals')
    op.drop_index('idx_approval_requested_by', table_name='approvals')
    op.drop_index('idx_approval_requested_by_status', table_name='approvals')
    op.drop_index('idx_approval_status_current_level', table_name='approvals')

    op.drop_index('idx_activity_entity_id', table_name='activity_logs')
    op.drop_index('idx_activity_entity_type', table_name='activity_logs')
    op.drop_index('idx_activity_action', table_name='activity_logs')
    op.drop_index('idx_activity_user_id', table_name='activity_logs')
    op.drop_index('idx_activity_user_id_created_at', table_name='activity_logs')
    op.drop_index('idx_activity_entity_type_entity_id', table_name='activity_logs')

    op.drop_index('idx_audit_timestamp', table_name='audit_logs')
    op.drop_index('idx_audit_entity_id', table_name='audit_logs')
    op.drop_index('idx_audit_entity', table_name='audit_logs')
    op.drop_index('idx_audit_action', table_name='audit_logs')
    op.drop_index('idx_audit_user_id', table_name='audit_logs')
    op.drop_index('idx_audit_user_id_timestamp', table_name='audit_logs')
    op.drop_index('idx_audit_entity_entity_id', table_name='audit_logs')

    op.drop_index('idx_comment_created_at', table_name='comments')
    op.drop_index('idx_comment_user_id', table_name='comments')
    op.drop_index('idx_comment_task_id', table_name='comments')
    op.drop_index('idx_comment_user_id_created_at', table_name='comments')
    op.drop_index('idx_comment_task_id_created_at', table_name='comments')

    op.drop_index('idx_notification_created_at', table_name='notifications')
    op.drop_index('idx_notification_is_read', table_name='notifications')
    op.drop_index('idx_notification_user_id', table_name='notifications')
    op.drop_index('idx_notification_user_id_created_at', table_name='notifications')
    op.drop_index('idx_notification_user_id_is_read', table_name='notifications')

    op.drop_index('idx_document_created_at', table_name='documents')
    op.drop_index('idx_document_uploaded_by', table_name='documents')
    op.drop_index('idx_document_task_id', table_name='documents')
    op.drop_index('idx_document_uploaded_by_created_at', table_name='documents')
    op.drop_index('idx_document_task_id_version', table_name='documents')

    op.drop_index('idx_task_history_changed_at', table_name='task_history')
    op.drop_index('idx_task_history_changed_by', table_name='task_history')
    op.drop_index('idx_task_history_task_id', table_name='task_history')
    op.drop_index('idx_task_history_task_id_changed_at', table_name='task_history')

    op.drop_index('idx_task_updated_at', table_name='tasks')
    op.drop_index('idx_task_created_at', table_name='tasks')
    op.drop_index('idx_task_priority', table_name='tasks')
    op.drop_index('idx_task_status', table_name='tasks')
    op.drop_index('idx_task_assigned_to_id', table_name='tasks')
    op.drop_index('idx_task_created_by_id', table_name='tasks')
    op.drop_index('idx_task_created_by_status', table_name='tasks')
    op.drop_index('idx_task_assigned_to_status', table_name='tasks')
    op.drop_index('idx_task_status_updated_at', table_name='tasks')

    op.drop_index('idx_user_role', table_name='users')
    op.drop_index('idx_user_is_active', table_name='users')
    op.drop_index('idx_user_role_active', table_name='users')
