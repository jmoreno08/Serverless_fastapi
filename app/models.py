from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDB(User):
    hashed_password: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    available: bool = True
