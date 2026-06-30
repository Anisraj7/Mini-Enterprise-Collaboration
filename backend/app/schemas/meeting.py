from datetime import datetime
from pydantic import BaseModel

from app.enums.meeting import MeetingStatus


class MeetingCreate(BaseModel):
    project_id: int
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime


class MeetingUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: MeetingStatus | None = None


class MeetingResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime
    status: MeetingStatus
    created_by: int

    model_config = {"from_attributes": True}