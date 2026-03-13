from pydantic import BaseModel, EmailStr
from typing import Optional, List
import uuid

class UserBase(BaseModel):
    nome: str
    email: EmailStr
    idade: int

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    idade: int | None = None

class User(UserBase):
    id: uuid.UUID

    class Config:
       from_attributes = True