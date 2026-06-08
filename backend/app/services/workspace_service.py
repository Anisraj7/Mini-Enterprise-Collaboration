from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.tenant_guard import TenantGuard

from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember

from app.repository.workspace_repository import (
    WorkspaceRepository,
)

from app.repository.workspace_member_repository import (
    WorkspaceMemberRepository,
)

from app.repository.tenant_collab_settings_repository import (
    TenantCollaborationSettingsRepository,
)

from app.utils.slug import slugify


class WorkspaceService:

    @staticmethod
    def create_workspace(
        db: Session,
        current_user,
        data,
    ):
        settings = (
            TenantCollaborationSettingsRepository
            .get_by_organization(
                db,
                current_user.organization_id,
            )
        )

        if settings and not settings.workspace_enabled:
            raise HTTPException(
                status_code=403,
                detail=(
                    "Workspace module is disabled "
                    "for this organization"
                ),
            )

        current_count = (
            WorkspaceRepository.count_by_organization(
                db,
                current_user.organization_id,
            )
        )

        if (
            settings
            and settings.max_workspaces is not None
            and current_count >= settings.max_workspaces
        ):
            raise HTTPException(
                status_code=400,
                detail="Workspace limit reached",
            )

        slug = slugify(data.name)

        existing = (
            WorkspaceRepository.get_by_slug(
                db,
                current_user.organization_id,
                slug,
            )
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Workspace already exists",
            )

        workspace = Workspace(
            organization_id=current_user.organization_id,
            name=data.name.strip(),
            slug=slug,
            description=data.description,
            avatar_url=data.avatar_url,
            visibility=data.visibility,
            created_by=current_user.id,
        )

        workspace = WorkspaceRepository.create(
            db,
            workspace,
        )

        # Automatically add creator as workspace admin
        membership = WorkspaceMember(
            workspace_id=workspace.id,
            user_id=current_user.id,
            role="WORKSPACE_ADMIN",
        )

        WorkspaceMemberRepository.create(
            db,
            membership,
        )

        return workspace

    @staticmethod
    def get_workspaces_stmt(
        db: Session,
        current_user,
    ):
        return WorkspaceRepository.get_by_organization(
            db,
            current_user.organization_id,
        )

    @staticmethod
    def get_workspace(
        db: Session,
        workspace_id: int,
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

        return workspace

    @staticmethod
    def archive_workspace(
        db: Session,
        workspace_id: int,
        current_user,
    ):
        workspace = WorkspaceService.get_workspace(
            db,
            workspace_id,
            current_user,
        )

        if workspace.is_archived:
            return workspace

        return WorkspaceRepository.archive(
            db,
            workspace,
        )

    @staticmethod
    def restore_workspace(
        db: Session,
        workspace_id: int,
        current_user,
    ):
        workspace = WorkspaceService.get_workspace(
            db,
            workspace_id,
            current_user,
        )

        if not workspace.is_archived:
            return workspace

        return WorkspaceRepository.restore(
            db,
            workspace,
        )

    @staticmethod
    def update_workspace(
        db: Session,
        workspace_id: int,
        payload,
        current_user,
    ):
        workspace = WorkspaceService.get_workspace(
            db,
            workspace_id,
            current_user,
        )

        if payload.name is not None:

            new_name = payload.name.strip()

            slug = slugify(new_name)

            existing = (
                WorkspaceRepository.get_by_slug(
                    db,
                    current_user.organization_id,
                    slug,
                )
            )

            if (
                existing
                and existing.id != workspace.id
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Workspace already exists",
                )

            workspace.name = new_name
            workspace.slug = slug

        if payload.description is not None:
            workspace.description = payload.description

        if payload.avatar_url is not None:
            workspace.avatar_url = payload.avatar_url

        if payload.visibility is not None:
            workspace.visibility = payload.visibility

        return WorkspaceRepository.update(
            db,
            workspace,
        )