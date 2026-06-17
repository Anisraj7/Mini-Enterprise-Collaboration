from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


ALLOWED_WORKSPACE_ROLES = {
    "WORKSPACE_ADMIN",
    "MANAGER",
    "EMPLOYEE",
}


class WorkspaceMemberCreate(BaseModel):
    user_id: int = Field(
        ...,
        gt=0,
    )

    role: str = Field(
        default="EMPLOYEE",
    )

    @field_validator("role")
    @classmethod
    def validate_role(
        cls,
        value: str,
    ) -> str:
        value = value.upper()

        if value not in ALLOWED_WORKSPACE_ROLES:
            raise ValueError(
                "Role must be WORKSPACE_ADMIN, MANAGER, or EMPLOYEE"
            )

        return value


class WorkspaceMemberRoleUpdate(BaseModel):
    role: str

    @field_validator("role")
    @classmethod
    def validate_role(
        cls,
        value: str,
    ) -> str:
        value = value.upper()

        if value not in ALLOWED_WORKSPACE_ROLES:
            raise ValueError(
                "Role must be WORKSPACE_ADMIN, MANAGER, or EMPLOYEE"
            )

        return value


class WorkspaceMemberResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    workspace_id: int
    user_id: int

    user_name: str | None = None
    user_email: str | None = None

    role: str
    joined_at: datetime
    is_active: bool