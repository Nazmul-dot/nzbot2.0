"""
DTOs (Pydantic schemas) = the public "contract" of the API.

These are what clients actually send/receive over HTTP.
They are deliberately kept separate from the ORM model (user_model.py)
so you can change your DB schema without breaking your API, and vice versa.
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr
    password: str
    is_active: bool = True


class LoginDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str

class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime

class UserUpdateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None
    created_at: datetime | None = None