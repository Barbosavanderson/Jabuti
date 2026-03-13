from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List

from app.db.session import SessionLocal
from app.crud import usuarios as crud
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get
@router.get("/", response_model=List[User])
def lista_usuarios(limit: int = 12, offset: int = 0, db: Session = Depends(get_db)):
    return crud.get_usuarios(db, limit=limit, offset=offset)

@router.get("/{id}", response_model=User)
def obter_usuario(id: uuid.UUID, db: Session = Depends(get_db)):
    usuario = crud.get_usuario(db, id=id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# Post
@router.post("/", response_model=User)
def criar_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db, usuario)

# Put
@router.put("/{id}", response_model=User)
def atualizar_usuario(id: uuid.UUID, usuario: UserUpdate, db: Session = Depends(get_db)):
    usuario_atualizado = crud.update_usuario(db, id=id, usuario=usuario)
    if not usuario_atualizado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario_atualizado

# Delete
@router.delete("/{id}")
def deletar_usuario(id: uuid.UUID, db: Session = Depends(get_db)):
    sucesso = crud.delete_usuario(db, id=id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"ok": True}
