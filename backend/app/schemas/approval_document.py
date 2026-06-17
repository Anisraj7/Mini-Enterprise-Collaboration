from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApprovalDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    approval_id: int

    file_name: str
    file_path: str
    file_size: int
    mime_type: str

    uploaded_by: int
    document_type: str

    created_at: datetime


class ApprovalDocumentUploadResponse(BaseModel):
    message: str
    document_id: int