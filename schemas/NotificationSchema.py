from pydantic import BaseModel

# Notification-related schema
class NotificationBase(BaseModel):
    message: str

class NotificationCreate(NotificationBase):
    patient_id: int

class Notification(NotificationBase):
    id: int
    patient_id: int

    class Config:
        from_attributes = True
