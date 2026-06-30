from datetime import datetime
from pydantic import BaseModel


class AIMeetingSummaryCreate(BaseModel):
    summary: str | None = None
    action_items: str | None = None
    risks: str | None = None
    decisions: str | None = None


class AIMeetingSummaryResponse(BaseModel):
    id: int
    meeting_id: int
    summary: str | None
    action_items: str | None
    risks: str | None
    decisions: str | None
    generated_at: datetime

    model_config = {"from_attributes": True}