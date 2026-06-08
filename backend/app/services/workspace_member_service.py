from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.tenant_guard import TenantGuard

from app.models.workspace_member import (
    WorkspaceMember,
)

from app.repository.workspace_member_repository import (
    WorkspaceMemberRepository,
)

from app.repository.workspace_repository import (
    WorkspaceRepository,
)

from app.repository.user_repository import (
    UserRepository,
)

from app.repository.tenant_collab_settings_repository import (
    TenantCollaborationSettingsRepository,
)


ALLOWED_WORKSPACE_ROLES = {
    "WORKSPACE_ADMIN",
    "MANAGER",
    "EMPLOYEE",
}


class WorkspaceMemberService:

    @staticmethod
    def add_member(
        db: Session,
        workspace_id: int,
        user_id: int,
        current_user,
        role: str = "EMPLOYEE",
    ):
        workspace = WorkspaceRepository.get_by_id(
            db,
            workspace_id,
        )

        if not workspace:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found",
            )

        TenantGuard.validate(
            current_user,
            workspace.organization_id,
        )

        user = UserRepository.get_by_id(
            db,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        TenantGuard.validate(
            user,
            workspace.organization_id,
        )

        role = role.upper()

        if role not in ALLOWED_WORKSPACE_ROLES:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Role must be "
                    "WORKSPACE_ADMIN, MANAGER, or EMPLOYEE"
                ),
            )

        existing = (
            WorkspaceMemberRepository.get_member(
                db,
                workspace_id,
                user_id,
            )
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="User already exists in workspace",
            )

        settings = (
            TenantCollaborationSettingsRepository
            .get_by_organization(
                db,
                workspace.organization_id,
            )
        )

        member_count = (
            WorkspaceMemberRepository
            .count_active_members(
                db,
                workspace_id,
            )
        )

        if (
            settings
            and settings.max_workspace_members is not None
            and member_count >= settings.max_workspace_members
        ):
            raise HTTPException(
                status_code=400,
                detail="Workspace member limit reached",
            )

        member = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role,
        )

        return WorkspaceMemberRepository.create(
            db,
            member,
        )

    @staticmethod
    def get_members_stmt(
        db: Session,
        workspace_id: int,
        current_user,
        search: str | None = None,
    ):
        workspace = WorkspaceRepository.get_by_id(
            db,
            workspace_id,
        )

        if not workspace:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found",
            )

        TenantGuard.validate(
            current_user,
            workspace.organization_id,
        )

        return (
            WorkspaceMemberRepository
            .get_workspace_members(
                db,
                workspace_id,
                search,
            )
        )

    @staticmethod
    def update_role(
        db: Session,
        workspace_id: int,
        user_id: int,
        current_user,
        role: str,
    ):
        workspace = WorkspaceRepository.get_by_id(
            db,
            workspace_id,
        )

        if not workspace:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found",
            )

        TenantGuard.validate(
            current_user,
            workspace.organization_id,
        )

        member = (
            WorkspaceMemberRepository.get_member(
                db,
                workspace_id,
                user_id,
            )
        )

        if not member:
            raise HTTPException(
                status_code=404,
                detail="Workspace member not found",
            )

        role = role.upper()

        if role not in ALLOWED_WORKSPACE_ROLES:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Role must be "
                    "WORKSPACE_ADMIN, MANAGER, or EMPLOYEE"
                ),
            )

        if (
            member.role == "WORKSPACE_ADMIN"
            and role != "WORKSPACE_ADMIN"
        ):
            admin_count = (
                WorkspaceMemberRepository
                .count_workspace_admins(
                    db,
                    workspace_id,
                )
            )

            if admin_count <= 1:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Cannot remove the last "
                        "workspace admin"
                    ),
                )

        member.role = role

        return WorkspaceMemberRepository.update(
            db,
            member,
        )

    @staticmethod
    def remove_member(
        db: Session,
        workspace_id: int,
        user_id: int,
        current_user,
    ):
        workspace = WorkspaceRepository.get_by_id(
            db,
            workspace_id,
        )

        if not workspace:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found",
            )

        TenantGuard.validate(
            current_user,
            workspace.organization_id,
        )

        member = (
            WorkspaceMemberRepository.get_member(
                db,
                workspace_id,
                user_id,
            )
        )

        if not member:
            raise HTTPException(
                status_code=404,
                detail="Workspace member not found",
            )

        if member.role == "WORKSPACE_ADMIN":
            admin_count = (
                WorkspaceMemberRepository
                .count_workspace_admins(
                    db,
                    workspace_id,
                )
            )

            if admin_count <= 1:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Cannot remove the last "
                        "workspace admin"
                    ),
                )

        WorkspaceMemberRepository.delete(
            db,
            member,
        )

        return {
            "message": (
                "Member removed successfully"
            )
        }