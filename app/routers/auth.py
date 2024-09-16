from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from app.utils.auth import create_access_token, verify_password
from app.models.models import LoginRequest
from app.utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

users_db = {
    "john": {
        "username": "john",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    }
}

@router.post("/login")
def login(login_data: LoginRequest):
    """
    Autentica a un usuario verificando el nombre de usuario y la contraseña proporcionados.

    Este endpoint verifica si el nombre de usuario existe en la base de datos de usuarios y si la 
    contraseña proporcionada coincide con la contraseña hash almacenada. Si la autenticación es 
    exitosa, genera un token de acceso que expira después de una duración predefinida.

    Args:
        login_data (LoginRequest): La solicitud de inicio de sesión que contiene el nombre de usuario y la contraseña.

    Raises:
        HTTPException: Si las credenciales son inválidas, se lanza una excepción 401 Unauthorized.

    Returns:
        dict: Un diccionario que contiene el token de acceso y su tipo. Ejemplo:
              {
                "access_token": "<token>",
                "token_type": "bearer"
              }
    """
    db_user = users_db.get(login_data.username)
    if not db_user or not verify_password(login_data.password, db_user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": login_data.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}
