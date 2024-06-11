from pydantic import BaseModel
from typing import Optional

# Patient-related schema
class PatientBase(BaseModel):
    name: str
    user_id: int
    medical_record: str
    nik: str
    gender: str
    address: str
    telephone: str
    date_of_birth: str
    allergy: str
    allergy_year: str
    bpjs_status: bool
    height: int
    weight: int
    bmi: float
    age: int

class PatientUpdate(BaseModel):
    name: Optional[str]
    nik: Optional[str]
    gender: Optional[str]
    address: Optional[str]
    telephone: Optional[str]
    date_of_birth: Optional[str]
    medical_record: Optional[str]
    bmi: Optional[float]
    height: Optional[int]
    weight: Optional[int]
    age: Optional[int]

class PatientCreate(PatientBase):
    password: str

class PatientLogin(BaseModel):
    username: str
    password: str

class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True
