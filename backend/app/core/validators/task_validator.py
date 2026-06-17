from fastapi import (
    HTTPException,
    status,
)

from app.models.workspace_member import (
    WorkspaceMember,
)

from app.models.channel_member import (
    ChannelMember,
)


class TaskValidator:

    @staticmethod
    def validate_workspace_assignee(
        member: WorkspaceMember | None,
    ) -> None:

        if member is None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Assignee must belong "
                    "to workspace"
                ),
            )

        if not member.is_active:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Workspace membership inactive"
                ),
            )

    @staticmethod
    def validate_channel_assignee(
        member: ChannelMember | None,
    ) -> None:

        if member is None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Assignee must belong "
                    "to channel"
                ),
            )