from pydantic import BaseModel

# Review-related schema
class ReviewBase(BaseModel):
    text: str
    date: str
    star: int

class ReviewCreate(ReviewBase):
    patient_id: int
    doctor_id: int

class Review(ReviewBase):
    id: int
    patient_id: int
    doctor_id: int

    class Config:
        from_attributes = True
