from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import (
    paginate,
)

from sqlalchemy.orm import Session

from app.core.permissions import require_roles

from app.db.database import get_db

from app.models.enums import UserRole

from app.schemas.workspace_member import (
    WorkspaceMemberCreate,
    WorkspaceMemberResponse,
    WorkspaceMemberRoleUpdate,
)

from app.services.workspace_member_service import (
    WorkspaceMemberService,
)

router = APIRouter()


read_roles = [
    UserRole.ORGANIZATION_ADMIN.value,
    UserRole.WORKSPACE_ADMIN.value,
    UserRole.MANAGER.value,
    UserRole.EMPLOYEE.value,
]

manage_roles = [
    UserRole.ORGANIZATION_ADMIN.value,
    UserRole.WORKSPACE_ADMIN.value,
]

member_add_roles = [
    UserRole.ORGANIZATION_ADMIN.value,
    UserRole.WORKSPACE_ADMIN.value,
    UserRole.MANAGER.value,
]


@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberResponse,
)
def add_workspace_member(
    workspace_id: int,
    payload: WorkspaceMemberCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(member_add_roles)
    ),
):
    return WorkspaceMemberService.add_member(
        db,
        workspace_id,
        payload.user_id,
        current_user,
        payload.role,
    )


@router.get(
    "/{workspace_id}/members",
    response_model=Page[WorkspaceMemberResponse],
)
def get_workspace_members(
    workspace_id: int,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(read_roles)
    ),
):
    return paginate(
        db,
        WorkspaceMemberService.get_members_stmt(
            db,
            workspace_id,
            current_user,
            search,
        ),
    )


@router.patch(
    "/{workspace_id}/members/{user_id}/role",
    response_model=WorkspaceMemberResponse,
)
def update_member_role(
    workspace_id: int,
    user_id: int,
    payload: WorkspaceMemberRoleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(manage_roles)
    ),
):
    return WorkspaceMemberService.update_role(
        db,
        workspace_id,
        user_id,
        current_user,
        payload.role,
    )


@router.delete(
    "/{workspace_id}/members/{user_id}",
)
def remove_member(
    workspace_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(manage_roles)
    ),
):
    return WorkspaceMemberService.remove_member(
        db,
        workspace_id,
        user_id,
        current_user,
    )