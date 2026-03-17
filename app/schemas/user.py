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
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    idade: Optional[int] = None

class User(UserBase):
    id: uuid.UUID

    class Config:
       from_attributes = True
class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        orm_mode = True

class PfinacaoUsuarios(BaseModel):
    totalItems: int
    pages: int
    size: int
    totalPages: int
    data: List[UsuarioOut]