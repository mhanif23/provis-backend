from pydantic import BaseModel

# Doctor-related schema
class DoctorBase(BaseModel):
    name: str
class DoctorCreate(DoctorBase):
    specialty: str
    hospital: str
    experience: str
    philosophy: str
    innovation: str
class Doctor(DoctorBase):
    id: int
    hospital: str
    experience: str
    philosophy: str
    innovation: str
    
    class Config:
        from_attributes = True
