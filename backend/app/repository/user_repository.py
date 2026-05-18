from sqlalchemy.orm import Session

from app.models.user import User


def get_users_query(db: Session, organization_id: int | None = None):
    query = db.query(User)

    if organization_id:
        query = query.filter(User.organization_id == organization_id)

    return query


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_assignable_users_query(db: Session, current_user: User):
    query = db.query(User)

    if current_user.organization_id:
        query = query.filter(
            User.organization_id == current_user.organization_id
        )

    return query.filter(User.role.in_(["manager", "employee"]))

