from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.models.user import User


def get_user_by_email(
    db: Session,
    email: str,
):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user_repository(
    db: Session,
    user: User,
):

    db.add(user)

    db.flush()

    return user


def create_refresh_token_repository(
    db: Session,
    refresh_token: RefreshToken,
):

    db.add(refresh_token)

    return refresh_token