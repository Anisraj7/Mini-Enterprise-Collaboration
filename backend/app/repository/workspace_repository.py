from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.orm import Session

from app.models.workspace import Workspace


class WorkspaceRepository:

    @staticmethod
    def create(
        db: Session,
        workspace: Workspace,
    ) -> Workspace:
        db.add(workspace)

        db.commit()

        db.refresh(workspace)

        return workspace

    @staticmethod
    def get_by_id(
        db: Session,
        workspace_id: int,
    ) -> Workspace | None:
        stmt = select(Workspace).where(
            Workspace.id == workspace_id
        )

        return (
            db.execute(stmt)
            .scalar_one_or_none()
        )

    @staticmethod
    def get_by_slug(
        db: Session,
        organization_id: int,
        slug: str,
    ) -> Workspace | None:
        stmt = select(Workspace).where(
            Workspace.organization_id == organization_id,
            Workspace.slug == slug,
        )

        return (
            db.execute(stmt)
            .scalar_one_or_none()
        )

    @staticmethod
    def get_by_organization(
        db: Session,
        organization_id: int,
    ):
        return (
            select(Workspace)
            .where(
                Workspace.organization_id == organization_id
            )
            .order_by(
                Workspace.created_at.desc()
            )
        )

    @staticmethod
    def count_by_organization(
        db: Session,
        organization_id: int,
    ) -> int:
        stmt = select(
            func.count(Workspace.id)
        ).where(
            Workspace.organization_id == organization_id,
            Workspace.is_archived.is_(False),
        )

        return (
            db.execute(stmt)
            .scalar_one()
        )

    @staticmethod
    def update(
        db: Session,
        workspace: Workspace,
    ) -> Workspace:
        db.commit()

        db.refresh(workspace)

        return workspace

    @staticmethod
    def archive(
        db: Session,
        workspace: Workspace,
    ) -> Workspace:
        workspace.is_archived = True

        db.commit()

        db.refresh(workspace)

        return workspace

    @staticmethod
    def restore(
        db: Session,
        workspace: Workspace,
    ) -> Workspace:
        workspace.is_archived = False

        db.commit()

        db.refresh(workspace)

        return workspace