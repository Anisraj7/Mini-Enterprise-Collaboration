from sqlalchemy import (
    func,
    select,
    or_,
)

from sqlalchemy.orm import Session

from app.models.workspace_member import (
    WorkspaceMember,
)
from app.models.user import User

class WorkspaceMemberRepository:

    @staticmethod
    def create(
        db: Session,
        member: WorkspaceMember,
    ) -> WorkspaceMember:
        db.add(member)

        db.commit()

        db.refresh(member)

        return member

    @staticmethod
    def get_member(
        db: Session,
        workspace_id: int,
        user_id: int,
    ) -> WorkspaceMember | None:
        stmt = select(
            WorkspaceMember
        ).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )

        return (
            db.execute(stmt)
            .scalar_one_or_none()
        )

    @staticmethod
    def get_workspace_members(
        db: Session,
        workspace_id: int,
        search: str | None = None,
    ):
        stmt = (
            select(WorkspaceMember)
            .join(
                User,
                User.id == WorkspaceMember.user_id,
            )
            .where(
                WorkspaceMember.workspace_id == workspace_id
            )
        )

        if search:
            stmt = stmt.where(
                or_(
                    User.name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            )

        return stmt.order_by(
            WorkspaceMember.joined_at.desc()
        )

    @staticmethod
    def count_active_members(
        db: Session,
        workspace_id: int,
    ) -> int:
        stmt = select(
            func.count(WorkspaceMember.id)
        ).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.is_active.is_(True),
        )

        return (
            db.execute(stmt)
            .scalar_one()
        )

    @staticmethod
    def get_workspace_admins(
        db: Session,
        workspace_id: int,
    ):
        return (
            select(WorkspaceMember)
            .where(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.role == "WORKSPACE_ADMIN",
                WorkspaceMember.is_active.is_(True),
            )
        )

    @staticmethod
    def update(
        db: Session,
        member: WorkspaceMember,
    ) -> WorkspaceMember:
        db.commit()

        db.refresh(member)

        return member

    @staticmethod
    def delete(
        db: Session,
        member: WorkspaceMember,
    ) -> None:
        db.delete(member)

        db.commit()
        
    @staticmethod
    def count_workspace_admins(
        db: Session,
        workspace_id: int,
    ) -> int:
        stmt = select(
            func.count(WorkspaceMember.id)
        ).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.role == "WORKSPACE_ADMIN",
            WorkspaceMember.is_active.is_(True),
        )

        return db.execute(stmt).scalar_one()