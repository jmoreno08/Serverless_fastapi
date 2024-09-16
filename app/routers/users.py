from fastapi import APIRouter, Depends, HTTPException
from app.models.models import User, UserInDB
from app.utils.auth import get_password_hash, get_current_user
import uuid
from datetime import datetime
import pytz

router = APIRouter()

users_db = {}

@router.post("")
def create_user(user: User, current_user: User = Depends(get_current_user)):

    """
    Crea un nuevo usuario en la base de datos después de validar los datos proporcionados.

    Este endpoint permite crear un nuevo usuario. Primero, se verifica que el nombre de usuario y 
    la contraseña no sean `None`. Luego, se asegura de que el nombre de usuario no exista ya en la 
    base de datos. Si todas las validaciones son correctas, se establece la fecha y hora de creación 
    del usuario en UTC y se genera un nuevo UUID. A continuación, se hash la contraseña proporcionada 
    y se almacena el nuevo usuario en la base de datos.

    Args:
        user (User): El objeto que contiene la información del nuevo usuario, incluyendo nombre de usuario y contraseña.

    Raises:
        HTTPException: 
            - Si el nombre de usuario es `None`, se lanza una excepción 400 Bad Request con el detalle "username cannot be None".
            - Si el nombre de usuario ya existe, se lanza una excepción 400 Bad Request con el detalle "Username already exists".
            - Si la contraseña es `None`, se lanza una excepción 400 Bad Request con el detalle "Password cannot be None".

    Returns:
        dict: Un diccionario que contiene el UUID del usuario, el nombre de usuario y la fecha de creación. Ejemplo:
              {
                "userid": "<uuid>",
                "username": "<nombre_de_usuario>",
                "created_by": "<fecha_y_hora>"
              }
    """

    if user.username is None:
        raise HTTPException(status_code=400, detail="username cannot be None")

    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if user.password is None:
        raise HTTPException(status_code=400, detail="Password cannot be None")
    
    user.created_at = datetime.now(pytz.utc)  # Establece la fecha y hora en UTC
    user.userid = uuid.uuid4()  # Genera un nuevo UUID

    
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(**user.model_dump(), hashed_password=hashed_password)
    users_db[user.username] = user_in_db

    return { "userid":user.userid ,"username": user.username, "created_by": user.created_at}

@router.get("")
def get_users(current_user: User = Depends(get_current_user)):

    """
    Obtiene una lista de todos los usuarios en la base de datos.

    Este endpoint recupera todos los usuarios almacenados en la base de datos. Para cada usuario,
    se crea un diccionario con los campos seleccionados (`userid`, `username`, `hashed_password`, 
    `created_at`, `updated_at`). Se eliminan los campos vacíos (`created_at` y `updated_at`) si 
    no están presentes.

    Args:
        current_user (User): El usuario actualmente autenticado que realiza la solicitud, obtenido mediante la dependencia `get_current_user`.

    Raises:
        HTTPException: Si no se encuentran usuarios en la base de datos, se lanza una excepción 404 Not Found.

    Returns:
        list: Una lista de diccionarios que representan los usuarios. Cada diccionario contiene los campos 
              `userid`, `username`, `hashed_password`, `created_at` y `updated_at`, con los campos vacíos eliminados si es necesario.
    """

    users = []

    for u in users_db.values():
        user_dict = u.dict(include={"userid", "username", "hashed_password", "created_at", "updated_at"})
        
        # Elimina los campos vacíos
        if not user_dict.get("created_at"):
            user_dict.pop("created_at", None)
        if not user_dict.get("updated_at"):
            user_dict.pop("updated_at", None)
        
        users.append(user_dict)

    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    return users



@router.get("/{userid}")
def get_user_id(userid: str, current_user: User = Depends(get_current_user)):

    """
    Obtiene los detalles de un usuario a partir de su `userid`.

    Este endpoint permite recuperar la información de un usuario almacenado en la base de datos 
    usando su `userid`. Primero, valida que el `userid` proporcionado no esté vacío. Luego, busca 
    al usuario en la base de datos. Si el usuario es encontrado, devuelve su información excluyendo 
    el campo `hashed_password`. Si no se encuentra al usuario, lanza una excepción 404 Not Found.

    Args:
        userid (str): El identificador único (UUID) del usuario.
        current_user (User): El usuario actualmente autenticado que realiza la solicitud, obtenido mediante la dependencia `get_current_user`.

    Raises:
        HTTPException:
            - Si `userid` está vacío o en blanco, lanza una excepción 400 Bad Request con el detalle "El user_id no puede estar vacío".
            - Si no se encuentra al usuario en la base de datos, lanza una excepción 404 Not Found con el detalle "User not found".

    Returns:
        dict: Un diccionario que contiene la información del usuario excluyendo su contraseña hash. Ejemplo:
              {
                "userid": "<uuid>",
                "username": "<nombre_de_usuario>",
                "created_at": "<fecha_y_hora>",
                "updated_at": "<fecha_y_hora>"
              }
    """

    # Validación de que userid no esté vacío
    if not userid or userid.strip() == "":
        raise HTTPException(status_code=400, detail="El user_id no puede estar vacío")
    
    user_in_db = users_db.get(userid)

    if user_in_db:
        return user_in_db.dict(exclude={"hashed_password"})
    
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{userid}")
def update_user(userid: str, user: User, current_user: User = Depends(get_current_user)):
    """
    Actualiza los detalles de un usuario existente en la base de datos.

    Este endpoint permite actualizar el nombre de usuario y la contraseña de un usuario existente.
    Primero, valida que el `userid` proporcionado no esté vacío. Luego, busca al usuario en la base 
    de datos. Si el usuario es encontrado, actualiza los campos proporcionados y establece la fecha 
    y hora de actualización en UTC. Si no se encuentra al usuario, lanza una excepción 404 Not Found.

    Args:
        userid (str): El identificador único (UUID) del usuario.
        user (User): El objeto que contiene la nueva información del usuario, incluyendo nombre de usuario y contraseña.
        current_user (User): El usuario actualmente autenticado que realiza la solicitud, obtenido mediante la dependencia `get_current_user`.

    Raises:
        HTTPException:
            - Si `userid` está vacío o en blanco, lanza una excepción 400 Bad Request con el detalle "El user_id no puede estar vacío".
            - Si no se encuentra al usuario en la base de datos, lanza una excepción 404 Not Found con el detalle "User not found".

    Returns:
        dict: Un diccionario que contiene solo la información actualizada del usuario. Ejemplo:
              {
                "username": "<nombre_de_usuario>",
                "updated_at": "<fecha_y_hora>"
              }
    """
    # Validación de que userid no esté vacío
    if not userid or userid.strip() == "":
        raise HTTPException(status_code=400, detail="El user_id no puede estar vacío")

    user_in_db = users_db.get(userid)

    if user_in_db:
        updated_data = {}
        if user.username:
            user_in_db.username = user.username
            updated_data["username"] = user.username
        if user.password:
            user_in_db.hashed_password = get_password_hash(user.password)
            updated_data["password"] = "updated"
        user_in_db.updated_at = datetime.now(pytz.utc)  # Establece la fecha y hora de actualización en UTC
        updated_data["updated_at"] = user_in_db.updated_at

        return updated_data

    raise HTTPException(status_code=404, detail="User not found")

@router.patch("/{userid}")
def partial_update_user(username: str, current_user: User = Depends(get_current_user)):
    user_in_db = users_db.get(username)
    if user_in_db:
        return user_in_db.dict(exclude={"hashed_password"})
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{userid}")
def delete_user(username: str, current_user: User = Depends(get_current_user)):
    user_in_db = users_db.get(username)
    if user_in_db:
        return user_in_db.dict(exclude={"hashed_password"})
    raise HTTPException(status_code=404, detail="User not found")