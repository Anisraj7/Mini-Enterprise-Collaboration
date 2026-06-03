from fastapi import HTTPException

from app.core.tenant_guard import TenantGuard

from app.models.channel import Channel
from app.models.workspace import Workspace

from app.repository.channel_repository import (
    ChannelRepository
)


class ChannelService:

    @staticmethod
    def create_channel(
        db,
        current_user,
        data
    ):
        TenantGuard.validate(
            current_user,
            current_user.organization_id
        )

        channel = Channel(
            organization_id=current_user.organization_id,
            workspace_id=data.workspace_id,
            name=data.name,
            description=data.description,
            channel_type=data.channel_type,
            created_by=current_user.id
        )

        return ChannelRepository.create(
            db,
            channel
        )

    @staticmethod
    def get_channels(
        db,
        workspace_id,
        current_user
    ):
        workspace = (
            db.query(Workspace)
            .filter(Workspace.id == workspace_id)
            .first()
        )

        if workspace:
            TenantGuard.validate(
                current_user,
                workspace.organization_id
            )

        channels = (
            ChannelRepository.get_by_workspace(
                db,
                workspace_id
            )
        )

        return channels

    @staticmethod
    def get_channel(
        db,
        channel_id,
        current_user
    ):
        channel = (
            ChannelRepository.get_by_id(
                db,
                channel_id
            )
        )

        if not channel:
            raise HTTPException(
                status_code=404,
                detail="Channel not found"
            )

        TenantGuard.validate(
            current_user,
            channel.organization_id
        )

        return channel

    @staticmethod
    def archive_channel(
        db,
        channel,
        current_user
    ):
        TenantGuard.validate(
            current_user,
            channel.organization_id
        )

        channel.is_archived = True

        db.commit()
        db.refresh(channel)

        return channel

    @staticmethod
    def restore_channel(
        db,
        channel,
        current_user
    ):
        TenantGuard.validate(
            current_user,
            channel.organization_id
        )

        channel.is_archived = False

        db.commit()
        db.refresh(channel)

        return channel

    @staticmethod
    def update_channel(
        db,
        channel_id,
        payload,
        current_user
    ):
        channel = (
            ChannelService.get_channel(
                db,
                channel_id,
                current_user
            )
        )

        if payload.name is not None:
            channel.name = payload.name

        if payload.description is not None:
            channel.description = payload.description

        if payload.channel_type is not None:
            channel.channel_type = payload.channel_type

        db.commit()
        db.refresh(channel)

        return channel