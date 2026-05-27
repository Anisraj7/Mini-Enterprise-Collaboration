from fastapi import (
    Depends,
    HTTPException,
    status,
)

from app.core.dependencies import (
    get_current_user,
)

from app.models.user import User


# =========================================
# GENERIC ROLE CHECK
# =========================================
def require_roles(
    allowed_roles: list[str],
):

    def role_checker(
        current_user: User = Depends(
            get_current_user
        )
    ):

        if (
            current_user.role
            not in allowed_roles
        ):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker


# =========================================
# ADMIN ONLY
# =========================================
require_admin = require_roles(
    ["admin"]
)


# =========================================
# MANAGER OR ADMIN
# =========================================
require_manager_or_admin = (
    require_roles(
        [
            "admin",
            "manager",
        ]
    )
)


# =========================================
# AUDITOR OR ADMIN
# =========================================
require_auditor_or_admin = (
    require_roles(
        [
            "admin",
            "auditor",
        ]
    )
)