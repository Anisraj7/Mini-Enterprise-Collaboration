from pydantic import BaseModel

from app.enums.attendance import AttendanceStatus


class MeetingAttendeeCreate(BaseModel):
    user_id: int


class MeetingAttendeeResponse(BaseModel):
    id: int
    meeting_id: int
    user_id: int
    attendance_status: AttendanceStatus

    model_config = {"from_attributes": True}