from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)


class OrganizationCreate(BaseModel):
    name: str
    contact_email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    industry: Optional[str] = None
    plan: str = "basic"

    @field_validator("name")
    @classmethod
    def validate_name(
        cls,
        value: str
    ):
        if not value.strip():
            raise ValueError(
                "Organization name cannot be empty"
            )
        return value.strip()


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    industry: Optional[str] = None
    plan: Optional[str] = None
    status: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(
        cls,
        value: Optional[str]
    ):
        if value is not None and not value.strip():
            raise ValueError(
                "Organization name cannot be empty"
            )
        return value.strip() if value else value


class OrganizationOut(BaseModel):
    id: int
    name: str
    slug: str
    contact_email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    industry: Optional[str] = None
    plan: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True