from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class WorkspaceMessageCreate(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


class WorkspaceMessageUpdate(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


class WorkspaceMessageResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    organization_id: int

    workspace_id: int

    sender_id: int

    sender_name: str | None = None

    content: str

    edited_at: datetime | None = None

    deleted_at: datetime | None = None

    created_at: datetime

    updated_at: datetime