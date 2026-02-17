from pydantic import BaseModel
from typing import Optional

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    user_id: int

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteResponse(NoteBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True