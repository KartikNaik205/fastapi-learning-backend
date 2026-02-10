from fastapi import APIRouter, status
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    return {
        "message": "User created successfully",
        "user": user
    }

@router.get("/", status_code=status.HTTP_200_OK)
def get_users():
    return {
        "message": "Users fetched successfully",
        "users": []
    }
