from fastapi import HTTPException

from app.models.enums import UserRole

from app.repository.tenant_collab_settings_repository import (
    TenantCollaborationSettingsRepository,
)


class TenantCollaborationSettingsService:

    @staticmethod
    def validate_access(
        current_user,
        organization_id: int
    ):

        if current_user.role == UserRole.SUPER_ADMIN.value:
            return

        if current_user.organization_id != organization_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    @staticmethod
    def get_settings(
        db,
        organization_id: int,
        current_user
    ):
        TenantCollaborationSettingsService.validate_access(
            current_user,
            organization_id
        )

        settings = (
            TenantCollaborationSettingsRepository
            .get_by_organization(
                db,
                organization_id
            )
        )

        if not settings:
            raise HTTPException(
                status_code=404,
                detail="Collaboration settings not found"
            )

        return settings

    @staticmethod
    def update_settings(
        db,
        organization_id: int,
        payload,
        current_user
    ):
        TenantCollaborationSettingsService.validate_access(
            current_user,
            organization_id
        )

        settings = (
            TenantCollaborationSettingsRepository
            .get_by_organization(
                db,
                organization_id
            )
        )

        if not settings:
            raise HTTPException(
                status_code=404,
                detail="Collaboration settings not found"
            )

        settings.max_workspaces = (
            payload.max_workspaces
        )

        settings.max_channels_per_workspace = (
            payload.max_channels_per_workspace
        )

        settings.max_workspace_members = (
            payload.max_workspace_members
        )

        settings.max_storage_mb = (
            payload.max_storage_mb
        )

        settings.workspace_enabled = (
            payload.workspace_enabled
        )

        settings.channel_enabled = (
            payload.channel_enabled
        )

        return (
            TenantCollaborationSettingsRepository
            .update(
                db,
                settings
            )
        )