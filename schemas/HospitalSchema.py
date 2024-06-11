from pydantic import BaseModel

# Hospital-related schema
class HospitalBase(BaseModel):
    name: str
class HospitalCreate(HospitalBase):
    address: str
    longitude: str
    latitude: str
class Hospital(HospitalBase):
    id: int
    address: str
    longitude: str
    latitude: str
    
    class Config:
        from_attributes = True
