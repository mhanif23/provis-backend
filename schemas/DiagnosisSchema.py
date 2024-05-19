from pydantic import BaseModel

#Diagnosis-related schema
class DiagnosisBase(BaseModel):
    diagnosis_name: str
    recommendation: str
    medicine_recommendation: str

class DiagnosisCreate(DiagnosisBase):
    doctor_id: int
    patient_id: int

class Diagnosis(DiagnosisBase):
    id: int
    doctor_id: int
    patient_id: int

    class Config:
        from_attributes = True
