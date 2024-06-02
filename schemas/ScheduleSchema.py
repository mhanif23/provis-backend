from pydantic import BaseModel
from datetime import time
# Schedule-related schema
class ScheduleBase(BaseModel):
    reservation_num: int
    timestart: time
    timeend: time
    location: str
    status: str
    bpjs: bool

class ScheduleCreate(ScheduleBase):
    patient_id: int
    doctor_id: int

class Schedule(ScheduleBase):
    id: int
    patient_id: int
    doctor_id: int

    class Config:
        from_attributes = True
