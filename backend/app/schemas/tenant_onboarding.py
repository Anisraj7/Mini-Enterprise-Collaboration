from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)


class TenantOnboardRequest(BaseModel):
    organization_name: str
    organization_email: EmailStr

    admin_name: str
    admin_email: EmailStr
    password: str

    create_default_workspace: bool = True

    @field_validator(
        "organization_name",
        "admin_name"
    )
    @classmethod
    def validate_names(
        cls,
        value: str
    ):
        if not value.strip():
            raise ValueError(
                "Field cannot be empty"
            )
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: str
    ):
        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters"
            )
        return value


class TenantAdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("name")
    @classmethod
    def validate_name(
        cls,
        value: str
    ):
        if not value.strip():
            raise ValueError(
                "Name cannot be empty"
            )
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: str
    ):
        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters"
            )
        return value


class TenantOnboardingOut(BaseModel):
    id: int

    organization_id: int

    admin_user_id: Optional[int] = None

    onboarding_status: str

    default_workspace_created: bool

    settings_created: bool

    completed_at: Optional[datetime] = None

    created_at: datetime

    class Config:
        from_attributes = True