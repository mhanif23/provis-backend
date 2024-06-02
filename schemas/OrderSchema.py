from pydantic import BaseModel

# Order-related schema
class OrderBase(BaseModel):
    address: str
    courier: str
    payment: str
    bpjs: bool
    status: str

class OrderCreate(OrderBase):
    patient_id: int
    medicine_id: int

class Order(OrderBase):
    id: int
    patient_id: int
    medicine_id: int

    class Config:
        from_attributes = True
