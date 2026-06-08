from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.orm import Session

from app.models.channel import Channel


class ChannelRepository:

    @staticmethod
    def create(
        db: Session,
        channel: Channel,
    ) -> Channel:
        db.add(channel)

        db.commit()

        db.refresh(channel)

        return channel

    @staticmethod
    def get_by_id(
        db: Session,
        channel_id: int,
    ) -> Channel | None:
        stmt = select(Channel).where(
            Channel.id == channel_id
        )

        return (
            db.execute(stmt)
            .scalar_one_or_none()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        workspace_id: int,
        name: str,
    ) -> Channel | None:
        stmt = select(Channel).where(
            Channel.workspace_id == workspace_id,
            Channel.name == name,
        )

        return (
            db.execute(stmt)
            .scalar_one_or_none()
        )

    @staticmethod
    def get_by_workspace(
        workspace_id: int,
    ):
        return (
            select(Channel)
            .where(
                Channel.workspace_id == workspace_id
            )
            .order_by(
                Channel.created_at.desc()
            )
        )

    @staticmethod
    def count_by_workspace(
        db: Session,
        workspace_id: int,
    ) -> int:
        stmt = select(
            func.count(Channel.id)
        ).where(
            Channel.workspace_id == workspace_id,
            Channel.is_archived.is_(False),
        )

        return (
            db.execute(stmt)
            .scalar_one()
        )

    @staticmethod
    def update(
        db: Session,
        channel: Channel,
    ) -> Channel:
        db.commit()

        db.refresh(channel)

        return channel

    @staticmethod
    def archive(
        db: Session,
        channel: Channel,
    ) -> Channel:
        channel.is_archived = True

        db.commit()

        db.refresh(channel)

        return channel

    @staticmethod
    def restore(
        db: Session,
        channel: Channel,
    ) -> Channel:
        channel.is_archived = False

        db.commit()

        db.refresh(channel)

        return channel