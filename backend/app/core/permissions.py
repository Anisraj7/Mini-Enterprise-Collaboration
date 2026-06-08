from fastapi import (
    Depends,
    HTTPException,
    status,
)

from app.core.dependencies import (
    get_current_user,
)

from app.models.user import User

from app.models.enums import UserRole

ROLE_ALIASES = {
    "super_admin": UserRole.SUPER_ADMIN.value,
    "organization_admin": UserRole.ORGANIZATION_ADMIN.value,
    "workspace_admin": UserRole.WORKSPACE_ADMIN.value,
    "manager": UserRole.MANAGER.value,
    "employee": UserRole.EMPLOYEE.value,

    # backward compatibility
    "admin": UserRole.ORGANIZATION_ADMIN.value,
    "moderator": UserRole.MANAGER.value,
    "member": UserRole.EMPLOYEE.value,
    "viewer": UserRole.EMPLOYEE.value,
    "auditor": UserRole.ORGANIZATION_ADMIN.value,
}


def normalize_role(role: str | UserRole):
    if isinstance(role, UserRole):
        role = role.value

    normalized = str(role).strip().lower()
    return ROLE_ALIASES.get(normalized, normalized)


def require_roles(
    allowed_roles: list[str] | list[UserRole],
):
    normalized_allowed = {
        normalize_role(role)
        for role in allowed_roles
    }

    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        current_role = normalize_role(
            current_user.role
        )

        # Super Admin bypass
        if current_role == normalize_role(
            UserRole.SUPER_ADMIN
        ):
            return current_user

        if current_role not in normalized_allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker


# =========================================
# SUPER ADMIN ONLY
# =========================================
require_super_admin = require_roles(
    [UserRole.SUPER_ADMIN.value]
)

# =========================================
# ORGANIZATION ADMIN ONLY
# =========================================
require_organization_admin = require_roles(
    [UserRole.ORGANIZATION_ADMIN.value]
)

# =========================================
# WORKSPACE MANAGEMENT
# =========================================
require_workspace_admin = require_roles(
    [
        UserRole.ORGANIZATION_ADMIN.value,
        UserRole.WORKSPACE_ADMIN.value,
    ]
)

# =========================================
# MANAGER LEVEL ACCESS
# =========================================
require_manager = require_roles(
    [
        UserRole.ORGANIZATION_ADMIN.value,
        UserRole.WORKSPACE_ADMIN.value,
        UserRole.MANAGER.value,
    ]
)

# =========================================
# ANY AUTHENTICATED USER
# =========================================
require_employee = require_roles(
    [
        UserRole.ORGANIZATION_ADMIN.value,
        UserRole.WORKSPACE_ADMIN.value,
        UserRole.MANAGER.value,
        UserRole.EMPLOYEE.value,
    ]
)

# =========================================
# BACKWARD COMPATIBILITY
# =========================================
require_admin = require_organization_admin

require_manager_or_admin = require_manager

require_auditor_or_admin = require_employee