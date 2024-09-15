from fastapi import APIRouter, HTTPException
from app.models import User, UserInDB
from app.auth import get_password_hash

router = APIRouter()

# Base de datos simulada
users_db = {
    "john": {
        "username": "john",
        "hashed_password": "$2b$12$somethinghashed"
    }
}

# Ruta para crear un nuevo usuario
@router.post("/signup")
def create_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(**user.model_dump(), hashed_password=hashed_password)
    users_db[user.username] = user_in_db
    return {"username": user.username}

# Ruta para obtener información de un usuario
@router.get("/{username}")
def get_user(username: str):
    user = users_db.get(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")