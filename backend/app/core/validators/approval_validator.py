from fastapi import (
    HTTPException,
    status,
)

from app.models.user import User


class ApprovalValidator:

    @staticmethod
    def validate_access(
        current_user: User,
        requester_id: int,
        approver_id: int,
    ) -> None:

        allowed = (
            current_user.id == requester_id
            or current_user.id == approver_id
            or current_user.role
            == "ORGANIZATION_ADMIN"
        )

        if not allowed:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Not authorized "
                    "to access approval"
                ),
            )