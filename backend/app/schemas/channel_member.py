from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
)


class ChannelMemberResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    channel_id: int

    user_id: int

    joined_at: datetime

    is_muted: bool

    last_read_message_id: Optional[int]