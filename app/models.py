from pydantic import BaseModel, FieldValidationInfo, field_validator
from typing import Optional
import datetime
from zoneinfo import ZoneInfo  # Asegúrate de tener Python 3.9 o superior
import re
from uuid import UUID

class User(BaseModel):
    userid: UUID | None = None
    username: str
    password: str
    created_at : Optional[datetime.datetime] | None = None# 2032-04-23T10:20:30.400+02:30
    updated_at : Optional[datetime.datetime] | None = None# 2032-04-23T10:20:30.400+02:30
    


class UserInDB(User):
    hashed_password: str

# Modelo Pydantic para el login
class LoginRequest(BaseModel):
    username: str
    password: str
