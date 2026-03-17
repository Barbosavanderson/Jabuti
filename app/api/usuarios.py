from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.crud import usuarios
from app.db.session import get_db

router = APIRouter(prefix="/usuarios")

# paginação
@router.get("/")
def list_usuarios(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
      return usuarios.get_usuarios(db=db, limit=limit, offset=offset)

# usuário  ID
@router.get("/{user_id}")
def read_usuario(user_id: str, db: Session = Depends(get_db)):
    import uuid
    user_uuid = uuid.UUID(user_id)
    user = usuarios.get_usuario(db=db, id=user_uuid)
    if user:
        return user
    return {"error": "Usuário não encontrado"}

# Criar usuário
@router.post("/")
def create_usuario(usuario: usuarios.UserCreate, db: Session = Depends(get_db)):
    return usuarios.create_usuario(db=db, usuario=usuario)

# Atualizar usuário
@router.put("/{user_id}")
def update_usuario(user_id: str, usuario: usuarios.UserUpdate, db: Session = Depends(get_db)):
    import uuid
    user_uuid = uuid.UUID(user_id)
    updated = usuarios.update_usuario(db=db, id=user_uuid, usuario=usuario)
    if updated:
        return updated
    return {"error": "Usuário não encontrado"}

# Deletar usuário
@router.delete("/{user_id}")
def delete_usuario(user_id: str, db: Session = Depends(get_db)):
    import uuid
    user_uuid = uuid.UUID(user_id)
    deleted = usuarios.delete_usuario(db=db, id=user_uuid)
    if deleted:
        return {"status": "deletado"}
    return {"error": "Usuário não encontrado"}