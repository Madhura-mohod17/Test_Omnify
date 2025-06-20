from pydantic import BaseModel, EmailStr
from typing import List
from pydantic.config import ConfigDict

class AttendeeCreate(BaseModel):
    name: str
    email: EmailStr

class AttendeeOut(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class PaginationResponse(BaseModel):
    total_records: int
    total_pages: int
    current_page: int
    records_per_page: int
    record_start: int
    record_end: int

class PaginatedAttendeeResponse(BaseModel):
    attendees: List[AttendeeOut]
    pagination: PaginationResponse
