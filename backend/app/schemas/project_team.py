from datetime import datetime
from pydantic import BaseModel

from app.schemas.team import TeamResponse


class ProjectTeamCreate(BaseModel):
    team_id: int


class ProjectTeamResponse(BaseModel):
    id: int
    project_id: int
    team_id: int
    assigned_at: datetime
    team:TeamResponse

    model_config = {"from_attributes": True}