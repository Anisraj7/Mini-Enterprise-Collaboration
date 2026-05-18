from datetime import datetime, timedelta, timezone
import secrets

from fastapi import HTTPException, status

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
)

from app.models.refresh_token import RefreshToken
from app.models.password_reset import PasswordResetToken

from app.schemas.password_reset import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

from app.repository.auth_repository import (
    get_user_by_email,
    get_user_by_id,
    get_refresh_token,
    get_password_reset_token,
    create_refresh_token_repository,
    create_password_reset_token_repository,
)


def login_service(
    db: Session,
    email: str,
    password: str,
):

    db_user = get_user_by_email(
        db,
        email,
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(
        password,
        db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    access_token = create_access_token(
        {
            "sub": str(db_user.id),
            "role": db_user.role,
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": str(db_user.id),
        }
    )

    db_refresh_token = RefreshToken(
        user_id=db_user.id,
        token=refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )

    create_refresh_token_repository(
        db,
        db_refresh_token,
    )

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_access_token_service(
    db: Session,
    refresh_token: str,
):

    db_token = get_refresh_token(
        db,
        refresh_token,
    )

    now = datetime.now(timezone.utc)

    token_expiry = db_token.expires_at if db_token else None

    if token_expiry and token_expiry.tzinfo is None:
        token_expiry = token_expiry.replace(
            tzinfo=timezone.utc
        )

    if not db_token or (
        token_expiry
        and token_expiry < now
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    try:

        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from exc

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    user_id = payload.get("sub")

    user = get_user_by_id(
        db,
        int(user_id),
    )

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    new_access_token = create_access_token(
        {
            "sub": str(user_id),
            "role": user.role,
        }
    )

    return {
        "access_token": new_access_token
    }


def forgot_password_service(
    db: Session,
    data: ForgotPasswordRequest,
):

    user = get_user_by_email(
        db,
        data.email,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    reset_token = secrets.token_urlsafe(32)

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(minutes=15)
    )

    db_token = PasswordResetToken(
        user_id=user.id,
        token=reset_token,
        expires_at=expires_at,
    )

    create_password_reset_token_repository(
        db,
        db_token,
    )

    db.commit()

    return {
        "message": "Password reset token generated",
        "reset_token": reset_token,
    }


def reset_password_service(
    db: Session,
    data: ResetPasswordRequest,
):

    db_token = get_password_reset_token(
        db,
        data.token,
    )

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )

    if db_token.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token already used",
        )

    if db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expired",
        )

    user = get_user_by_id(
        db,
        db_token.user_id,
    )

    user.hashed_password = hash_password(
        data.new_password
    )

    db_token.is_used = True

    db.commit()

    return {
        "message": "Password reset successful"
    }