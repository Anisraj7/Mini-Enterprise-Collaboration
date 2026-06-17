from sqlalchemy import (
    or_,
    select,
)

from sqlalchemy.orm import (
    Session,
    joinedload,
)

from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.task import Task
from app.models.user import User


class TaskRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        task_id: int,
    ) -> Task | None:

        return (
            db.execute(
                select(Task)
                .options(
                    joinedload(
                        Task.assigned_to
                    )
                )
                .where(
                    Task.id == task_id
                )
            )
            .scalars()
            .first()
        )

    @staticmethod
    def visible_tasks_query(
        user: User,
    ):

        stmt = select(Task)

        if user.organization_id:

            stmt = stmt.where(
                Task.organization_id
                == user.organization_id
            )

        if user.role in (
            "SUPER_ADMIN",
            "ORGANIZATION_ADMIN",
            "WORKSPACE_ADMIN",
        ):
            return stmt

        if user.role == "MANAGER":

            return stmt.where(
                or_(
                    Task.created_by_id == user.id,
                    Task.assigned_to_id == user.id,
                )
            )

        return stmt.where(
            Task.assigned_to_id
            == user.id
        )

    @staticmethod
    def list_workspace_tasks(
        db: Session,
        workspace_id: int,
    ):

        stmt = (
            select(Task)
            .where(
                Task.workspace_id
                == workspace_id
            )
            .order_by(
                Task.created_at.desc()
            )
        )

        return paginate(
            db,
            stmt,
        )

    @staticmethod
    def list_channel_tasks(
        db: Session,
        channel_id: int,
    ):

        stmt = (
            select(Task)
            .where(
                Task.channel_id
                == channel_id
            )
            .order_by(
                Task.created_at.desc()
            )
        )

        return paginate(
            db,
            stmt,
        )

    @staticmethod
    def get_workspace_task(
        db: Session,
        workspace_id: int,
        task_id: int,
    ) -> Task | None:

        return (
            db.execute(
                select(Task)
                .where(
                    Task.workspace_id
                    == workspace_id
                )
                .where(
                    Task.id == task_id
                )
            )
            .scalar_one_or_none()
        )

    @staticmethod
    def get_channel_task(
        db: Session,
        channel_id: int,
        task_id: int,
    ) -> Task | None:

        return (
            db.execute(
                select(Task)
                .where(
                    Task.channel_id
                    == channel_id
                )
                .where(
                    Task.id == task_id
                )
            )
            .scalar_one_or_none()
        )

    @staticmethod
    def create(
        db: Session,
        task: Task,
    ) -> Task:

        db.add(task)

        db.commit()

        db.refresh(task)

        return task

    @staticmethod
    def update(
        db: Session,
        task: Task,
    ) -> Task:

        db.add(task)

        db.commit()

        db.refresh(task)

        return task

    @staticmethod
    def assign_task(
        db: Session,
        task: Task,
        assigned_to_id: int,
    ) -> Task:

        task.assigned_to_id = assigned_to_id

        db.add(task)

        db.commit()

        db.refresh(task)

        return task

    @staticmethod
    def delete(
        db: Session,
        task: Task,
    ) -> bool:

        db.delete(task)

        db.commit()

        return True

    @staticmethod
    def list_assignable_users(
        db: Session,
        user: User,
    ):

        stmt = select(User).where(
            User.is_active.is_(True)
        )

        if user.organization_id:

            stmt = stmt.where(
                User.organization_id
                == user.organization_id
            )

        if user.role == "MANAGER":

            stmt = stmt.where(
                User.role.in_(
                    [
                        "MANAGER",
                        "EMPLOYEE",
                    ]
                )
            )

        return (
            db.execute(stmt)
            .scalars()
            .all()
        )
        
    @staticmethod
    def commit_refresh(
        db: Session,
        task: Task,
    ) -> Task:

        db.commit()

        db.refresh(task)

        return task