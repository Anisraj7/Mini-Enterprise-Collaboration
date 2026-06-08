from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.core.tenant_guard import TenantGuard


def test_tenant_guard_allows_same_organization():
    user = SimpleNamespace(role="employee", organization_id=10)

    assert TenantGuard.validate(user, organization_id=10) is None


def test_tenant_guard_allows_super_admin_for_any_organization():
    user = SimpleNamespace(role="super_admin", organization_id=10)

    assert TenantGuard.validate(user, organization_id=99) is None


def test_tenant_guard_blocks_cross_organization_access():
    user = SimpleNamespace(role="employee", organization_id=10)

    with pytest.raises(HTTPException) as exc_info:
        TenantGuard.validate(user, organization_id=99)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Cross organization access denied"
