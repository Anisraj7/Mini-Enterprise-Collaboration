from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)

from fastapi.security import (
    OAuth2PasswordBearer,
)

from jose import (
    JWTError,
    jwt,
)

from sqlalchemy.orm import Session

from app.core.config import (
    ALGORITHM,
    SECRET_KEY,
)

from app.db.database import (
    get_db,
)

from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    request: Request,
    token: str = Depends(
        oauth2_scheme
    ),
    db: Session = Depends(get_db),
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        # =====================================
        # GET USER ID
        # =====================================
        user_id = payload.get("sub")

        # =====================================
        # VALIDATE TOKEN TYPE
        # =====================================
        token_type = payload.get("type")

        if token_type != "access":

            raise HTTPException(
                status_code=401,
                detail="Invalid token type",
            )

    except JWTError as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    # =====================================
    # VALIDATE USER ID
    # =====================================
    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )

    # =====================================
    # VALIDATE USER
    # =====================================
    if not user or not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive or missing",
        )

    # =====================================
    # ATTACH USER TO REQUEST STATE
    # =====================================
    request.state.user = user

    return user