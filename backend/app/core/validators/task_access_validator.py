from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.repository.workspace_member_repository import (
    WorkspaceMemberRepository,
)

from app.repository.channel_member_repository import (
    ChannelMemberRepository,
)


class TaskAccessValidator:

    @staticmethod
    def validate_workspace_access(
        db: Session,
        workspace_id: int,
        user_id: int,
    ):

        member = (
            WorkspaceMemberRepository.get_member(
                db,
                workspace_id,
                user_id,
            )
        )

        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a workspace member",
            )

        return member

    @staticmethod
    def validate_channel_access(
        db: Session,
        channel_id: int,
        user_id: int,
    ):

        member = (
            ChannelMemberRepository.get_member(
                db,
                channel_id,
                user_id,
            )
        )

        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a channel member",
            )

        return member

    @staticmethod
    def validate_workspace_assignee(
        db: Session,
        workspace_id: int,
        user_id: int,
    ):

        member = (
            WorkspaceMemberRepository.get_member(
                db,
                workspace_id,
                user_id,
            )
        )

        if not member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assignee must belong to workspace",
            )

    @staticmethod
    def validate_channel_assignee(
        db: Session,
        channel_id: int,
        user_id: int,
    ):

        member = (
            ChannelMemberRepository.get_member(
                db,
                channel_id,
                user_id,
            )
        )

        if not member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assignee must belong to channel",
            )