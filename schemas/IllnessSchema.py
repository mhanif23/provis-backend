from pydantic import BaseModel

# Illness-related schema
class IllnessBase(BaseModel):
    name: str
    category: str
    general_symptoms: str
    unique_symptoms: str
    extra_symptoms: str

class IllnessCreate(IllnessBase):
    pass

class Illness(IllnessBase):
    id: int

    class Config:
        from_attributes = True
