from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.tenant_guard import TenantGuard

from app.models.channel_member import (
    ChannelMember,
)

from app.repository.channel_member_repository import (
    ChannelMemberRepository,
)

from app.repository.channel_repository import (
    ChannelRepository,
)

from app.repository.user_repository import (
    UserRepository,
)

from app.repository.workspace_member_repository import (
    WorkspaceMemberRepository,
)


class ChannelMemberService:

    @staticmethod
    def join_channel(
        db: Session,
        channel_id: int,
        user_id: int,
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

        if channel.is_archived:
            raise HTTPException(
                status_code=400,
                detail="Channel is archived",
            )

        user = UserRepository.get_by_id(
            db,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        TenantGuard.validate(
            user,
            channel.organization_id,
        )

        workspace_member = (
            WorkspaceMemberRepository.get_member(
                db,
                channel.workspace_id,
                user_id,
            )
        )

        if not workspace_member:
            raise HTTPException(
                status_code=403,
                detail=(
                    "User must belong to the workspace "
                    "before joining channels"
                ),
            )

        existing = (
            ChannelMemberRepository.get_member(
                db,
                channel_id,
                user_id,
            )
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Already joined channel",
            )

        if channel.channel_type == "PRIVATE":
            raise HTTPException(
                status_code=403,
                detail=(
                    "Private channels require "
                    "an invitation"
                ),
            )

        member = ChannelMember(
            channel_id=channel_id,
            user_id=user_id,
        )

        return ChannelMemberRepository.create(
            db,
            member,
        )

    @staticmethod
    def leave_channel(
        db: Session,
        channel_id: int,
        user_id: int,
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

        user = UserRepository.get_by_id(
            db,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        TenantGuard.validate(
            user,
            channel.organization_id,
        )

        member = (
            ChannelMemberRepository.get_member(
                db,
                channel_id,
                user_id,
            )
        )

        if not member:
            raise HTTPException(
                status_code=404,
                detail="Channel membership not found",
            )

        ChannelMemberRepository.delete(
            db,
            member,
        )

        return {
            "message": (
                "Left channel successfully"
            )
        }

    @staticmethod
    def get_members_stmt(
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

        if (
            channel.channel_type == "PRIVATE"
            and not ChannelMemberRepository.is_member(
                db,
                channel_id,
                current_user.id,
            )
        ):
            raise HTTPException(
                status_code=403,
                detail=(
                    "Private channel access denied"
                ),
            )

        return (
            ChannelMemberRepository
            .get_channel_members(
                db,
                channel_id,
            )
        )