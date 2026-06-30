from datetime import date, datetime
from pydantic import BaseModel

from app.enums.project import (
    ProjectPriority,
    ProjectStatus,
)


class ProjectCreate(BaseModel):
    workspace_id: int
    owner_id: int
    name: str
    description: str | None = None
    priority: ProjectPriority = ProjectPriority.MEDIUM
    start_date: date | None = None
    end_date: date | None = None


class ProjectUpdate(BaseModel):
    owner_id: int | None = None
    name: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None
    priority: ProjectPriority | None = None
    start_date: date | None = None
    end_date: date | None = None


class ProjectResponse(BaseModel):
    id: int
    organization_id: int
    workspace_id: int
    owner_id: int
    name: str
    description: str | None
    status: ProjectStatus
    priority: ProjectPriority
    start_date: date | None
    end_date: date | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}