from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from typing import List
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        name = user.name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail="User not found")
    
    if user_update.name is not None:
        user.name = user_update.name

    if user_update.email is not None:
        user.email = user_update.email

    db.commit()
    db.refresh(user)
    return user
