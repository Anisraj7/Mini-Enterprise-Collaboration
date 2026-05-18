from sqlalchemy.orm import Session, joinedload

from app.models.user import User
from app.models.organization import Organization
from app.models.refresh_token import RefreshToken
from app.models.password_reset import PasswordResetToken


def get_user_by_email(
    db: Session,
    email: str,
):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int,
):

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_with_organization(
    db: Session,
    user_id: int,
):

    return (
        db.query(User)
        .options(joinedload(User.organization))
        .filter(User.id == user_id)
        .first()
    )


def get_organization_by_name(
    db: Session,
    organization_name: str,
):

    return (
        db.query(Organization)
        .filter(Organization.name == organization_name)
        .first()
    )


def get_refresh_token(
    db: Session,
    token: str,
):

    return (
        db.query(RefreshToken)
        .filter(RefreshToken.token == token)
        .first()
    )


def get_password_reset_token(
    db: Session,
    token: str,
):

    return (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token == token)
        .first()
    )


def create_user_repository(
    db: Session,
    user: User,
):

    db.add(user)

    db.flush()

    return user


def create_organization_repository(
    db: Session,
    organization: Organization,
):

    db.add(organization)

    db.flush()

    return organization


def create_refresh_token_repository(
    db: Session,
    refresh_token: RefreshToken,
):

    db.add(refresh_token)

    return refresh_token


def create_password_reset_token_repository(
    db: Session,
    reset_token: PasswordResetToken,
):

    db.add(reset_token)

    return reset_token


def commit_refresh(
    db: Session,
    model,
):

    db.commit()

    db.refresh(model)

    return model