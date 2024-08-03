from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str
    first_name: str
    last_name: str
    age: Optional[int] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    model_config = {
        "from_attributes": True
    }

class UserInDBBase(UserBase):
    id: int
    age: Optional[int] = None
    address: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class User(UserInDBBase):
    name: str
    first_name: str
    last_name: str
    age: Optional[int]
    address: Optional[str]

    model_config = {
        "from_attributes": True
    }
