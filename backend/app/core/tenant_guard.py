from fastapi import HTTPException

from app.models.enums import UserRole


class TenantGuard:

    @staticmethod
    def validate(
        current_user,
        organization_id: int
    ):
        """
        Prevent cross-organization access.

        SUPER_ADMIN can access all organizations.

        All other users can only access
        resources belonging to their own
        organization.
        """

        if (
            current_user.role
            == UserRole.SUPER_ADMIN.value
        ):
            return

        if (
            current_user.organization_id
            != organization_id
        ):
            raise HTTPException(
                status_code=403,
                detail="Cross organization access denied"
            )