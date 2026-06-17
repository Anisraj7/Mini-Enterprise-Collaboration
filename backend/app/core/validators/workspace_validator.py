from fastapi import (
    HTTPException,
    status,
)

from app.models.workspace_member import (
    WorkspaceMember,
)


class WorkspaceValidator:

    @staticmethod
    def validate_member(
        member: WorkspaceMember | None,
    ) -> None:

        if member is None:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a workspace member",
            )

        if not member.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Workspace membership inactive",
            )

    @staticmethod
    def validate_admin(
        member: WorkspaceMember | None,
    ) -> None:

        WorkspaceValidator.validate_member(
            member
        )

        if member.role != "ADMIN":

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Workspace admin access required",
            )