from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ScheduleCreate(BaseModel):
    date: str  # YYYY-MM-DD
    title: str
    description: str = ""

class ScheduleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class ScheduleResponse(BaseModel):
    id: int
    user_id: int
    date: date
    title: str
    description: str
    is_completed: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
