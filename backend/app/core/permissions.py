from app.core.dependencies import get_current_user

from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from app.core.config import (
    ALGORITHM,
    SECRET_KEY,
)

from app.db.database import get_db

from app.models.user import User

# ROLE-BASED ACCESS CONTROL
def require_role(allowed_roles: list[str]):

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):

        if current_user.role not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker