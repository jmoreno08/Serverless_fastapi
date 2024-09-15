from fastapi import APIRouter
from app.models import User, UserInDB
from app.auth import get_password_hash

router = APIRouter()

users_db = {}

@router.post("/signup")
def create_user(user: User):
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(**user.model_dump(), hashed_password=hashed_password)
    users_db[user.username] = user_in_db
    return {"username": user.username}

@router.get("/{username}")
def get_user(username: str):
    user = users_db.get(username)
    if user:
        return user
    return {"error": "User not found"}
