from datetime import (
    datetime,
    timedelta,
    timezone,
)

import secrets

from urllib.parse import urlencode

from fastapi import (
    HTTPException,
    status,
)

from authlib.integrations.starlette_client import (
    OAuth,
)

from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.core.config import (
    FRONTEND_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
)

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
)

from app.models.refresh_token import RefreshToken
from app.models.user import User

from app.repository.oauth_repository import (
    get_user_by_email,
    create_user_repository,
    create_refresh_token_repository,
)

oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=(
        "https://accounts.google.com/"
        ".well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid email profile",
    },
)


async def google_login_service(
    request,
):

    if (
        not GOOGLE_CLIENT_ID
        or not GOOGLE_CLIENT_SECRET
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth is not configured",
        )

    redirect_uri = request.url_for(
        "google_callback"
    )

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
    )


async def google_callback_service(
    request,
    db: Session,
):

    token = await oauth.google.authorize_access_token(
        request
    )

    user = token.get("userinfo")

    if (
        not user
        or not user.get("email")
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account did not provide an email",
        )

    db_user = get_user_by_email(
        db,
        user["email"],
    )

    if not db_user:

        db_user = User(
            name=(
                user.get("name")
                or user["email"].split("@")[0]
            ),
            email=user["email"],
            role="employee",
            hashed_password=hash_password(
                secrets.token_urlsafe(32)
            ),
            is_active=True,
        )

        create_user_repository(
            db,
            db_user,
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
        expires_at=(
            datetime.now(timezone.utc)
            + timedelta(days=7)
        ),
    )

    create_refresh_token_repository(
        db,
        db_refresh_token,
    )

    db.commit()

    params = urlencode(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    )

    return RedirectResponse(
        (
            f"{FRONTEND_URL.rstrip('/')}"
            f"/oauth/callback?{params}"
        )
    )