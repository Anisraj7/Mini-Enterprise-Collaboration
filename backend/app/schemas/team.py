from datetime import datetime
from pydantic import BaseModel, Field


class TeamCreate(BaseModel):
    workspace_id: int
    name: str = Field(..., max_length=255)
    description: str | None = None


class TeamUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class TeamResponse(BaseModel):
    id: int
    organization_id: int
    workspace_id: int
    name: str
    description: str | None
    created_by: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}