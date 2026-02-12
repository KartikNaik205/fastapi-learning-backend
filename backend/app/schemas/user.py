from pydantic import BaseModel
from typing import Optional
class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(UserCreate):
    id: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
