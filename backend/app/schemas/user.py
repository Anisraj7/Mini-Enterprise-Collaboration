from enum import Enum
from typing import Optional
import re

import bleach
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.organization import OrganizationOut


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Anis Raj"])

    email: EmailStr

    role: UserRole = UserRole.employee

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        cleaned = bleach.clean(value.strip())

        if not cleaned:
            raise ValueError("Name cannot be empty")

        return cleaned


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)

    organization_id: Optional[int] = None

    organization_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=120
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")

        return value


class UserUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    role: Optional[UserRole] = None

    is_active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):

        if value is None:
            return value

        return bleach.clean(value.strip())


class UserLogin(BaseModel):
    email: EmailStr

    password: str = Field(..., min_length=1, max_length=128)


class UserSummary(BaseModel):
    id: int

    name: str

    email: EmailStr

    role: UserRole

    is_active: bool

    class Config:
        from_attributes = True


class UserOut(UserSummary):
    organization_id: Optional[int] = None

    organization: Optional[OrganizationOut] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str

    refresh_token: str

    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str

    role: str

    exp: int