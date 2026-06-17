from fastapi import (
    HTTPException,
    status,
)


class TenantValidator:

    @staticmethod
    def validate(
        user_organization_id: int,
        resource_organization_id: int,
    ) -> None:

        if (
            user_organization_id
            != resource_organization_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cross-tenant access denied",
            )