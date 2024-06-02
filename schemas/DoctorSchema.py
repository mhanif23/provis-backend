from pydantic import BaseModel

# Doctor-related schema
class DoctorBase(BaseModel):
    name: str
    user_id: int
class DoctorCreate(DoctorBase):
    specialty: str
    hospital: int
    experience: str
    philosophy: str
    innovation: str
class Doctor(DoctorBase):
    id: int
    specialty: str
    hospital: int
    experience: str
    philosophy: str
    innovation: str
    
    class Config:
        from_attributes = True
