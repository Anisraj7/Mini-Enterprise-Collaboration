from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.orm import Session

from app.models.channel_member import (
    ChannelMember,
)


class ChannelMemberRepository:

    @staticmethod
    def create(
        db: Session,
        member: ChannelMember,
    ) -> ChannelMember:
        db.add(member)

        db.commit()

        db.refresh(member)

        return member

    @staticmethod
    def get_member(
        db: Session,
        channel_id: int,
        user_id: int,
    ) -> ChannelMember | None:
        stmt = select(
            ChannelMember
        ).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == user_id,
        )

        return (
            db.execute(stmt)
            .scalar_one_or_none()
        )

    @staticmethod
    def get_channel_members(
        db: Session,
        channel_id: int,
    ):
        return (
            select(ChannelMember)
            .where(
                ChannelMember.channel_id == channel_id
            )
            .order_by(
                ChannelMember.joined_at.desc()
            )
        )

    @staticmethod
    def count_members(
        db: Session,
        channel_id: int,
    ) -> int:
        stmt = select(
            func.count(ChannelMember.id)
        ).where(
            ChannelMember.channel_id == channel_id
        )

        return (
            db.execute(stmt)
            .scalar_one()
        )

    @staticmethod
    def is_member(
        db: Session,
        channel_id: int,
        user_id: int,
    ) -> bool:
        return (
            ChannelMemberRepository.get_member(
                db,
                channel_id,
                user_id,
            )
            is not None
        )

    @staticmethod
    def update(
        db: Session,
        member: ChannelMember,
    ) -> ChannelMember:
        db.commit()

        db.refresh(member)

        return member

    @staticmethod
    def delete(
        db: Session,
        member: ChannelMember,
    ) -> None:
        db.delete(member)

        db.commit()