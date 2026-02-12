from fastapi import APIRouter, status, HTTPException
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from typing import List
import uuid


router = APIRouter(prefix="/users", tags=["Users"])

fake_users_db = []

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    new_user = {
        "id": str(uuid.uuid4()),
        "name": user.name,
        "email": user.email
    }

    fake_users_db.append(new_user)
    return new_user

@router.get("/", response_model=List[UserResponse])
def get_users():
    return fake_users_db


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    for index, user in enumerate(fake_users_db):
        if user["id"] == user_id:
           fake_users_db.pop(index)
           return
    raise HTTPException(status_code=404, detail="User not found")

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_update: UserUpdate):
    for user in fake_users_db:
        if user["id"] == user_id:
            if user_update.name is not None:
                user["name"] = user_update.name
            if user_update.email is not None:
                user["email"] = user_update.email
            return user
    raise HTTPException(status_code=404, detail="User not found")