from pydantic import BaseModel

# Hospital-related schema
class HospitalBase(BaseModel):
    name: str
class HospitalCreate(HospitalBase):
    address: str
    longitude: int
    latitude: str
class Hospital(HospitalBase):
    id: int
    address: str
    longitude: int
    latitude: str
    
    class Config:
        from_attributes = True
