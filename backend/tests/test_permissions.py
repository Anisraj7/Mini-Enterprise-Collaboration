from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.core.permissions import normalize_role, require_roles
from app.models.enums import UserRole


def test_normalize_role_accepts_enum_and_backward_compatible_aliases():
    assert normalize_role(UserRole.SUPER_ADMIN) == "super_admin"
    assert normalize_role("admin") == "organization_admin"
    assert normalize_role(" Moderator ") == "manager"
    assert normalize_role("viewer") == "employee"


def test_require_roles_allows_matching_user_role():
    checker = require_roles([UserRole.MANAGER])
    user = SimpleNamespace(role="manager")

    assert checker(current_user=user) is user


def test_require_roles_allows_super_admin_bypass():
    checker = require_roles([UserRole.EMPLOYEE])
    user = SimpleNamespace(role="super_admin")

    assert checker(current_user=user) is user


def test_require_roles_rejects_unauthorized_role():
    checker = require_roles([UserRole.ORGANIZATION_ADMIN])
    user = SimpleNamespace(role="employee")

    with pytest.raises(HTTPException) as exc_info:
        checker(current_user=user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Insufficient permissions"
