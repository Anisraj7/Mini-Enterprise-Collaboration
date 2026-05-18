from fastapi import (
    APIRouter,
    Depends,
    Request,
    status,
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from pydantic import BaseModel

from app.core.dependencies import get_current_user

from app.core.rate_limit import limiter

from app.db.database import get_db

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserOut,
)

from app.schemas.password_reset import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

from app.services.auth_service import (
    login_service,
    refresh_access_token_service,
    forgot_password_service,
    reset_password_service,
  
)

from app.services.user_service import (
    register_service,
    get_me_service,
    )

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("3/minute")
def register(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return register_service(
        db,
        user,
    )


@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return login_service(
        db,
        form_data.username,
        form_data.password,
    )


@router.get(
    "/me",
    response_model=UserOut,
)
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_me_service(
        db,
        current_user,
    )


@router.post("/refresh")
@limiter.limit("10/minute")
def refresh_access_token(
    request: Request,
    data: RefreshRequest,
    db: Session = Depends(get_db),
):
    return refresh_access_token_service(
        db,
        data.refresh_token,
    )


@router.post("/forgot-password")
@limiter.limit("3/minute")
def forgot_password(
    request: Request,
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    return forgot_password_service(
        db,
        data,
    )


@router.post("/reset-password")
@limiter.limit("5/minute")
def reset_password(
    request: Request,
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    return reset_password_service(
        db,
        data,
    )