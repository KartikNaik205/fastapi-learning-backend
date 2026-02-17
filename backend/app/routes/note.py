from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Note, User
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == note.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_note = Note(
        title=note.title,
        content=note.content,
        user_id=note.user_id
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

@router.get("/", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note

@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if note_update.title is not None:
        note.title = note_update.title
    
    if note_update.content is not None:
        note.content = note_update.content

    db.commit()
    db.refresh(note)
    
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()

    return