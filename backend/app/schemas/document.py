from pydantic import BaseModel
from datetime import datetime

class DocumentOut(BaseModel):
    id: int
    file_name: str
    version: int
    task_id: int
    created_at: datetime

    class Config:
        from_attributes = True