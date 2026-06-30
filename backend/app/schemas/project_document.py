from datetime import datetime
from pydantic import BaseModel

from app.enums.document import ProjectDocumentType


class ProjectDocumentResponse(BaseModel):
    id: int
    project_id: int
    file_name: str
    file_size: int
    mime_type: str
    document_type: ProjectDocumentType
    uploaded_by: int
    created_at: datetime

    model_config = {"from_attributes": True}