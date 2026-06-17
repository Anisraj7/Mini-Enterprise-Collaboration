from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.channel_message import ChannelMessage


class ChannelMessageRepository:

    @staticmethod
    def create(
        db: Session,
        message: ChannelMessage,
    ) -> ChannelMessage:

        db.add(message)

        db.commit()

        db.refresh(message)

        return message

    @staticmethod
    def get_by_id(
        db: Session,
        message_id: int,
    ) -> ChannelMessage | None:

        stmt = (
            select(ChannelMessage)
            .where(
                ChannelMessage.id == message_id
            )
        )

        result = db.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    def list_by_channel(
        db: Session,
        channel_id: int,
    ):

        stmt = (
            select(ChannelMessage)
            .where(
                ChannelMessage.channel_id == channel_id
            )
            .where(
                ChannelMessage.deleted_at.is_(None)
            )
            .order_by(
                ChannelMessage.created_at.desc()
            )
        )

        return paginate(
            db,
            stmt,
        )

    @staticmethod
    def update_content(
        db: Session,
        message: ChannelMessage,
        content: str,
    ) -> ChannelMessage:

        message.content = content
        message.edited_at = datetime.utcnow()

        db.commit()

        db.refresh(message)

        return message

    @staticmethod
    def soft_delete(
        db: Session,
        message: ChannelMessage,
    ) -> ChannelMessage:

        message.deleted_at = datetime.utcnow()

        db.commit()

        db.refresh(message)

        return message

    @staticmethod
    def get_channel_messages_count(
        db: Session,
        channel_id: int,
    ) -> int:

        stmt = (
            select(ChannelMessage)
            .where(
                ChannelMessage.channel_id == channel_id
            )
            .where(
                ChannelMessage.deleted_at.is_(None)
            )
        )

        result = db.execute(stmt)

        return len(
            result.scalars().all()
        )