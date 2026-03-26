import uuid
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import usuarios as usuarios_crud
from app.schemas.user import UserCreate, UserUpdate, User
from app.db.session import get_db

router = APIRouter(prefix="/usuarios")

# Listagem com paginação
@router.get("/")
def list_usuarios(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
      return usuarios_crud.get_usuarios(db=db, limit=limit, offset=offset)

# Buscar usuário por ID
@router.get("/{user_id}", response_model=User)
def read_usuario(user_id: str, db: Session = Depends(get_db)):
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="UUID inválido") from exc

    user = usuarios_crud.get_usuario(db=db, id=user_uuid)
    if user:
        return user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

# Criar usuário
@router.post("/", response_model=User)
def create_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    return usuarios_crud.create_usuario(db=db, usuario=usuario)

# Atualizar usuário
@router.put("/{user_id}", response_model=User)
def update_usuario(user_id: str, usuario: UserUpdate, db: Session = Depends(get_db)):
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="UUID inválido") from exc

    updated = usuarios_crud.update_usuario(db=db, id=user_uuid, usuario=usuario)
    if updated:
        return updated
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

# Deletar usuário
@router.delete("/{user_id}")
def delete_usuario(user_id: str, db: Session = Depends(get_db)):
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="UUID inválido") from exc

    deleted = usuarios_crud.delete_usuario(db=db, id=user_uuid)
    if deleted:
        return {"status": "deletado"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")