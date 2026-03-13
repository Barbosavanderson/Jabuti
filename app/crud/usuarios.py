

from sqlalchemy.orm import Session
from app.models import user
from app.schemas.user import UserCreate, UserUpdate
import uuid


#paginação
def get_usuarios(db: Session, limit: int = 12, offset: int = 0):
    return db.query(user.User).offset(offset).limit(limit).all()

#buscar por id
def get_usuario(db: Session, id: uuid.UUID):
    return db.query(user.User).filter(user.User.id == id).first()

#Novo
def create_usuario(db: Session, usuario: UserCreate):
    novo_usuario = user.User(
        id=uuid.uuid4(),
        nome=usuario.nome,
        email=usuario.email,
        idade=usuario.idade
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

#Atualizar
def update_usuario(db: Session, id: uuid.UUID, usuario: UserUpdate):
    db_usuario = db.query(user.User).filter(user.User.id == id).first()
    if not db_usuario:
        return None
    
    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

#deletar
def delete_usuario(db: Session, id: uuid.UUID):
    db_usuario = db.query(user.User).filter(user.User.id == id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True
    return False