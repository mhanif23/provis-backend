from pydantic import BaseModel

# Medicine-related schema
class MedicineBase(BaseModel):
    name: str
    manufacturer: str
    dosage: str
    description: str
    instruction: str
    price: int

class MedicineCreate(MedicineBase):
    pass

class Medicine(MedicineBase):
    id: int

    class Config:
        from_attributes = True
