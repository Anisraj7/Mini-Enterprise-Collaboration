from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.tenant_guard import TenantGuard

from app.models.channel import Channel
from app.models.channel_member import ChannelMember

from app.repository.channel_repository import (
    ChannelRepository,
)

from app.repository.channel_member_repository import (
    ChannelMemberRepository,
)

from app.repository.workspace_repository import (
    WorkspaceRepository,
)

from app.repository.workspace_member_repository import (
    WorkspaceMemberRepository,
)

from app.repository.tenant_collab_settings_repository import (
    TenantCollaborationSettingsRepository,
)


MANAGE_CHANNEL_ROLES = {
    "SUPER_ADMIN",
    "ORGANIZATION_ADMIN",
    "WORKSPACE_ADMIN",
    "MANAGER",
}


class ChannelService:

    @staticmethod
    def _can_manage_channels(
        current_user,
    ) -> bool:
        return (
            current_user.role.upper()
            in MANAGE_CHANNEL_ROLES
        )

    @staticmethod
    def create_channel(
        db: Session,
        current_user,
        data,
    ):
        workspace = WorkspaceRepository.get_by_id(
            db,
            data.workspace_id,
        )

        if not workspace:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found",
            )

        if workspace.is_archived:
            raise HTTPException(
                status_code=400,
                detail="Workspace is archived",
            )

        TenantGuard.validate(
            current_user,
            workspace.organization_id,
        )

        workspace_member = (
            WorkspaceMemberRepository.get_member(
                db,
                workspace.id,
                current_user.id,
            )
        )

        if not workspace_member:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You must belong to the workspace "
                    "to create channels"
                ),
            )

        settings = (
            TenantCollaborationSettingsRepository
            .get_by_organization(
                db,
                workspace.organization_id,
            )
        )

        if settings and not settings.channel_enabled:
            raise HTTPException(
                status_code=403,
                detail=(
                    "Channel module is disabled "
                    "for this organization"
                ),
            )

        channel_count = (
            ChannelRepository.count_by_workspace(
                db,
                workspace.id,
            )
        )

        if (
            settings
            and settings.max_channels_per_workspace is not None
            and channel_count >= settings.max_channels_per_workspace
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Channel limit reached "
                    "for this workspace"
                ),
            )

        existing = (
            ChannelRepository.get_by_name(
                db,
                workspace.id,
                data.name.strip(),
            )
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Channel already exists "
                    "in this workspace"
                ),
            )

        channel = Channel(
            organization_id=workspace.organization_id,
            workspace_id=workspace.id,
            name=data.name.strip(),
            description=data.description,
            channel_type=data.channel_type,
            created_by=current_user.id,
        )

        channel = ChannelRepository.create(
            db,
            channel,
        )

        creator_membership = ChannelMember(
            channel_id=channel.id,
            user_id=current_user.id,
        )

        ChannelMemberRepository.create(
            db,
            creator_membership,
        )

        return channel

    @staticmethod
    def get_channels_stmt(
        db: Session,
        workspace_id: int,
        current_user,
    ):
        workspace = WorkspaceRepository.get_by_id(
            db,
            workspace_id,
        )

        if not workspace:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found",
            )

        TenantGuard.validate(
            current_user,
            workspace.organization_id,
        )

        return ChannelRepository.get_by_workspace(
            workspace_id,
        )   

    @staticmethod
    def get_channel(
        db: Session,
        channel_id: int,
        current_user,
    ):
        channel = ChannelRepository.get_by_id(
            db,
            channel_id,
        )

        if not channel:
            raise HTTPException(
                status_code=404,
                detail="Channel not found",
            )

        TenantGuard.validate(
            current_user,
            channel.organization_id,
        )

        if channel.channel_type == "PRIVATE":

            if ChannelService._can_manage_channels(
                current_user
            ):
                return channel

            member = (
                ChannelMemberRepository.get_member(
                    db,
                    channel.id,
                    current_user.id,
                )
            )

            if not member:
                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Private channel access denied"
                    ),
                )

        return channel

    @staticmethod
    def update_channel(
        db: Session,
        channel_id: int,
        payload,
        current_user,
    ):
        channel = ChannelService.get_channel(
            db,
            channel_id,
            current_user,
        )

        if payload.name is not None:

            existing = (
                ChannelRepository.get_by_name(
                    db,
                    channel.workspace_id,
                    payload.name.strip(),
                )
            )

            if (
                existing
                and existing.id != channel.id
            ):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Channel already exists "
                        "in this workspace"
                    ),
                )

            channel.name = payload.name.strip()

        if payload.description is not None:
            channel.description = payload.description

        if payload.channel_type is not None:
            channel.channel_type = payload.channel_type

        return ChannelRepository.update(
            db,
            channel,
        )

    @staticmethod
    def archive_channel(
        db: Session,
        channel_id: int,
        current_user,
    ):
        channel = ChannelService.get_channel(
            db,
            channel_id,
            current_user,
        )

        if channel.is_archived:
            return channel

        return ChannelRepository.archive(
            db,
            channel,
        )

    @staticmethod
    def restore_channel(
        db: Session,
        channel_id: int,
        current_user,
    ):
        channel = ChannelService.get_channel(
            db,
            channel_id,
            current_user,
        )

        if not channel.is_archived:
            return channel

        return ChannelRepository.restore(
            db,
            channel,
        )