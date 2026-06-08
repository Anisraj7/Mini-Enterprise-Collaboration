from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class TenantCollaborationUsageResponse(BaseModel):
    id: int

    organization_id: int

    workspace_count: int = Field(
        ge=0
    )

    channel_count: int = Field(
        ge=0
    )

    member_count: int = Field(
        ge=0
    )

    storage_used_mb: int = Field(
        ge=0
    )

    last_calculated_at: Optional[datetime] = None

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True