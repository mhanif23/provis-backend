from pydantic import BaseModel
from datetime import datetime

# Message-related schema
class MessageBase(BaseModel):
    datetime: datetime
    text: str

class MessageCreate(MessageBase):
    patient_id: int
    doctor_id: int

class Message(MessageBase):
    id: int
    patient_id: int
    doctor_id: int

    class Config:
        from_attributes = True
