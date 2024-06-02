# from pydantic import BaseModel

# # User-related schema
# class UserBase(BaseModel):
#     username: str
#     name: str
#     medical_record: str
#     nik: str
#     gender: str
#     address: str
#     telephone: str
#     date_of_birth: str
#     allergy: str
#     allergy_year: str
#     bpjs_status: bool

# class UserCreate(UserBase):
#     password: str

# class UserLogin(BaseModel):
#     username: str
#     password: str

# class User(UserBase):
#     id: int

#     class Config:
#         from_attributes = True

from pydantic import BaseModel

# User-related schema
class UserBase(BaseModel):
    username: str
    role: str
class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True
