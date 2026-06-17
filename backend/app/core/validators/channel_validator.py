from fastapi import (
    HTTPException,
    status,
)

from app.models.channel_member import (
    ChannelMember,
)


class ChannelValidator:

    @staticmethod
    def validate_member(
        member: ChannelMember | None,
    ) -> None:

        if member is None:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a channel member",
            )

    @staticmethod
    def validate_moderator(
        member: ChannelMember | None,
    ) -> None:

        ChannelValidator.validate_member(
            member
        )

        if member.role != "MODERATOR":

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Channel moderator access required",
            )