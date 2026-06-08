from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_users_query(
    db: Session,
    organization_id: int | None = None,
):
    query = select(User)

    if organization_id:
        query = query.where(
            User.organization_id == organization_id
        )

    return query


def get_user_by_id(
    db: Session,
    user_id: int,
):
    return (
        db.execute(select(User).where(
            User.id == user_id
        ))
        .scalars()
        .first()
    )


def get_assignable_users_query(
    db: Session,
    current_user: User,
):
    query = select(User)

    if current_user.organization_id:
        query = query.where(
            User.organization_id
            == current_user.organization_id
        )

    if current_user.role in (
        "super_admin",
        "organization_admin",
        "workspace_admin",
    ):
        return query.where(
            User.role.in_(
                [
                    "workspace_admin",
                    "manager",
                    "employee",
                ]
            )
        )

    if current_user.role == "manager":
        return query.where(
            User.role.in_(
                [
                    "manager",
                    "employee",
                ]
            )
        )

    return query.where(
        User.id == current_user.id
    )


class UserRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int,
    ):
        return get_user_by_id(
            db,
            user_id,
        )
