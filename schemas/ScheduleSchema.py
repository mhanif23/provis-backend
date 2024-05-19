from pydantic import BaseModel

# Schedule-related schema
class ScheduleBase(BaseModel):
    reservation_num: int
    time: str
    location: str

class ScheduleCreate(ScheduleBase):
    patient_id: int
    doctor_id: int

class Schedule(ScheduleBase):
    id: int
    patient_id: int
    doctor_id: int

    class Config:
        from_attributes = True
