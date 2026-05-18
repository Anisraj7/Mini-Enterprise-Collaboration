from datetime import datetime
from pydantic import BaseModel

class ActivityLogOut(BaseModel):

    id: int
    action: str
    entity_type: str
    entity_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        
class ActivityUser(BaseModel):

    id: int
    name: str

    class Config:
        from_attributes = True

