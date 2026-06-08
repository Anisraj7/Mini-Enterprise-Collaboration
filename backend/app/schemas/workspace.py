from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


ALLOWED_VISIBILITY = {
    "PUBLIC",
    "PRIVATE",
}


class WorkspaceCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
    )

    avatar_url: Optional[str] = Field(
        default=None,
        max_length=500,
    )

    visibility: str = Field(
        default="PRIVATE",
    )

    @field_validator("name")
    @classmethod
    def validate_name(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Workspace name cannot be empty"
            )

        return value

    @field_validator("visibility")
    @classmethod
    def validate_visibility(
        cls,
        value: str,
    ) -> str:
        value = value.upper()

        if value not in ALLOWED_VISIBILITY:
            raise ValueError(
                "Visibility must be PUBLIC or PRIVATE"
            )

        return value


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
    )

    avatar_url: Optional[str] = Field(
        default=None,
        max_length=500,
    )

    visibility: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(
        cls,
        value: Optional[str],
    ) -> Optional[str]:
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError(
                "Workspace name cannot be empty"
            )

        return value

    @field_validator("visibility")
    @classmethod
    def validate_visibility(
        cls,
        value: Optional[str],
    ) -> Optional[str]:
        if value is None:
            return value

        value = value.upper()

        if value not in ALLOWED_VISIBILITY:
            raise ValueError(
                "Visibility must be PUBLIC or PRIVATE"
            )

        return value


class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    organization_id: int

    name: str

    slug: str

    description: Optional[str]

    avatar_url: Optional[str]

    visibility: str

    created_by: int

    is_archived: bool

    created_at: datetime

    updated_at: datetime