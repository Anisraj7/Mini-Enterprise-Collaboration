from __future__ import annotations

from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.models.channel_message import ChannelMessage
from app.models.channel_member import ChannelMember

from app.repository.channel_message_repository import (
    ChannelMessageRepository,
)

from app.schemas.channel_message import (
    ChannelMessageCreate,
    ChannelMessageUpdate,
)
from app.repository.channel_repository import ChannelRepository


class ChannelMessageService:

    @staticmethod
    def validate_channel_member(
        channel_member: ChannelMember | None,
    ) -> None:

        if channel_member is None:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a channel member",
            )

    @staticmethod
    def validate_message_permission(
        message: ChannelMessage,
        channel_member: ChannelMember,
        current_user_id: int,
    ) -> None:

        is_sender = (
            message.sender_id == current_user_id
        )

        is_channel_moderator = (
            getattr(channel_member, "role", None)
            == "CHANNEL_MODERATOR"
        )

        is_workspace_admin = (
            getattr(channel_member, "role", None)
            == "WORKSPACE_ADMIN"
        )

        if not (
            is_sender
            or is_channel_moderator
            or is_workspace_admin
        ):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized",
            )

    @staticmethod
    def create_message(
        db: Session,
        organization_id: int,
        workspace_id: int,
        channel_id: int,
        sender_id: int,
        payload: ChannelMessageCreate,
    ) -> ChannelMessage:
        
        channel = ChannelRepository.get_by_id(
            db,
            channel_id,
        )
        
        if channel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found",
            )
        
        message = ChannelMessage(
            organization_id=organization_id,
            workspace_id=channel.workspace_id,
            channel_id=channel_id,
            sender_id=sender_id,
            content=payload.content,
        )

        return ChannelMessageRepository.create(
            db=db,
            message=message,
        )

    @staticmethod
    def get_message(
        db: Session,
        message_id: int,
    ) -> ChannelMessage | None:

        return ChannelMessageRepository.get_by_id(
            db=db,
            message_id=message_id,
        )

    @staticmethod
    def list_messages(
        db: Session,
        channel_id: int,
    ):

        return ChannelMessageRepository.list_by_channel(
            db=db,
            channel_id=channel_id,
        )

    @staticmethod
    def update_message(
        db: Session,
        message: ChannelMessage,
        payload: ChannelMessageUpdate,
    ) -> ChannelMessage:

        return ChannelMessageRepository.update_content(
            db=db,
            message=message,
            content=payload.content,
        )

    @staticmethod
    def delete_message(
        db: Session,
        message: ChannelMessage,
    ) -> ChannelMessage:

        return ChannelMessageRepository.soft_delete(
            db=db,
            message=message,
        )