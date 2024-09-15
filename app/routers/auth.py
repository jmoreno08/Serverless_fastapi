from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from app.auth import create_access_token, verify_password
from app.models import User
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

users_db = {
    "john": {
        "username": "john",
        "hashed_password": "$2b$12$somethinghashed"
    }
}

@router.post("/login")
def login(user: User):
    db_user = users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}
