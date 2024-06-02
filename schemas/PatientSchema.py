from pydantic import BaseModel

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

class PatientCreate(PatientBase):
    password: str

class PatientLogin(BaseModel):
    username: str
    password: str

class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True
