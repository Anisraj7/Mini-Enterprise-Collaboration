from datetime import datetime
from pydantic import BaseModel


class MeetingNoteCreate(BaseModel):
    notes: str


class MeetingNoteUpdate(BaseModel):
    notes: str


class MeetingNoteResponse(BaseModel):
    id: int
    meeting_id: int
    notes: str
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}