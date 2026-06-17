from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ChannelMessageCreate(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


class ChannelMessageUpdate(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


class ChannelMessageResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    organization_id: int

    workspace_id: int

    channel_id: int

    sender_id: int

    sender_name: str | None = None

    content: str

    edited_at: Optional[datetime] = None

    deleted_at: Optional[datetime] = None

    created_at: datetime

    updated_at: datetime