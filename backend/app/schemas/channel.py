from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


ALLOWED_CHANNEL_TYPES = {
    "PUBLIC",
    "PRIVATE",
    "ANNOUNCEMENT",
    "PROJECT",
}


class ChannelCreate(BaseModel):
    workspace_id: int = Field(
        ...,
        gt=0,
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
    )

    channel_type: str = Field(
        default="PUBLIC",
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
                "Channel name cannot be empty"
            )

        return value

    @field_validator("channel_type")
    @classmethod
    def validate_channel_type(
        cls,
        value: str,
    ) -> str:
        value = value.upper()

        if value not in ALLOWED_CHANNEL_TYPES:
            raise ValueError(
                "Channel type must be PUBLIC, PRIVATE, ANNOUNCEMENT, or PROJECT"
            )

        return value


class ChannelUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
    )

    channel_type: Optional[str] = None

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
                "Channel name cannot be empty"
            )

        return value

    @field_validator("channel_type")
    @classmethod
    def validate_channel_type(
        cls,
        value: Optional[str],
    ) -> Optional[str]:
        if value is None:
            return value

        value = value.upper()

        if value not in ALLOWED_CHANNEL_TYPES:
            raise ValueError(
                "Channel type must be PUBLIC, PRIVATE, ANNOUNCEMENT, or PROJECT"
            )

        return value


class ChannelResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    organization_id: int

    workspace_id: int

    name: str

    description: Optional[str]

    channel_type: str

    created_by: int

    is_archived: bool

    created_at: datetime

    updated_at: datetime