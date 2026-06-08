from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func, select

from app.models.enums import UserRole
from app.models.workspace_member import WorkspaceMember

from app.repository.channel_repository import (
    ChannelRepository,
)
from app.repository.tenant_collab_usage_repository import (
    TenantCollaborationUsageRepository,
)
from app.repository.workspace_repository import (
    WorkspaceRepository,
)


class TenantCollaborationUsageService:

    @staticmethod
    def validate_access(
        current_user,
        organization_id: int
    ):
        if (
            current_user.role
            != UserRole.SUPER_ADMIN.value
            and current_user.organization_id
            != organization_id
        ):
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    @staticmethod
    def get_usage(
        db,
        organization_id: int,
        current_user
    ):
        TenantCollaborationUsageService.validate_access(
            current_user,
            organization_id
        )

        usage = (
            TenantCollaborationUsageRepository
            .get_by_organization(
                db,
                organization_id
            )
        )

        if not usage:
            raise HTTPException(
                status_code=404,
                detail="Collaboration usage not found"
            )

        return usage

    @staticmethod
    def recalculate_usage(
        db,
        organization_id: int,
        current_user
    ):
        TenantCollaborationUsageService.validate_access(
            current_user,
            organization_id
        )

        usage = (
            TenantCollaborationUsageRepository
            .get_by_organization(
                db,
                organization_id
            )
        )

        if not usage:
            raise HTTPException(
                status_code=404,
                detail="Collaboration usage not found"
            )

        workspaces = (
            db.execute(WorkspaceRepository.get_by_organization(
                db,
                organization_id
            )).scalars().all()
        )

        workspace_count = len(workspaces)
        channel_count = 0
        member_count = 0

        for workspace in workspaces:

            channels = (
                db.execute(
                    ChannelRepository.get_by_workspace(
                        workspace.id
                    )
                )
                .scalars()
                .all()
            )

            channel_count += len(channels)

            member_count += (
                db.execute(select(func.count(WorkspaceMember.id)).where(
                    WorkspaceMember.workspace_id
                    == workspace.id,
                    WorkspaceMember.is_active.is_(True)
                )).scalar_one()
            )

        usage.workspace_count = workspace_count
        usage.channel_count = channel_count
        usage.member_count = member_count

        # Future file module can update this
        usage.storage_used_mb = (
            usage.storage_used_mb or 0
        )

        usage.last_calculated_at = (
            datetime.utcnow()
        )

        return (
            TenantCollaborationUsageRepository
            .update(
                db,
                usage
            )
        )
