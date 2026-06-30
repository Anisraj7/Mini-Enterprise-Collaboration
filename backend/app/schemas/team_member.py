from datetime import datetime
from pydantic import BaseModel

from app.enums.team import TeamMemberRole


class TeamMemberCreate(BaseModel):
    user_id: int
    role: TeamMemberRole = TeamMemberRole.MEMBER


class TeamMemberResponse(BaseModel):
    id: int
    team_id: int
    user_id: int
    role: TeamMemberRole
    joined_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}