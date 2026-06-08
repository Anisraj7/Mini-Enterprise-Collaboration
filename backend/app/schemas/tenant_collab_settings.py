from pydantic import (
    BaseModel,
    Field,
)


class TenantCollaborationSettingsUpdate(BaseModel):
    max_workspaces: int = Field(
        ...,
        ge=1
    )

    max_channels_per_workspace: int = Field(
        ...,
        ge=1
    )

    max_workspace_members: int = Field(
        ...,
        ge=1
    )

    max_storage_mb: int = Field(
        ...,
        ge=1
    )

    workspace_enabled: bool

    channel_enabled: bool


class TenantCollaborationSettingsResponse(BaseModel):
    id: int

    organization_id: int

    max_workspaces: int

    max_channels_per_workspace: int

    max_workspace_members: int

    max_storage_mb: int

    workspace_enabled: bool

    channel_enabled: bool

    class Config:
        from_attributes = True