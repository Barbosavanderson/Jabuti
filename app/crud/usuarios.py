from sqlalchemy.orm import Session
from app.models import user
from app.schemas.user import UserCreate, UserUpdate
from app.db.redis_config import redis_client
import uuid

# Paginação segura
def get_usuarios(db: Session, limit: int = 10, offset: int = 0):
    if limit < 1:
        limit = 10
    if offset < 0:
        offset = 0
     # Chave única para cada página
    key = f"usuarios:limit={limit}:offset={offset}"

    # Tenta buscar no Redis
    cached = redis_client.get(key)
    if cached:
        return {"data": cached, "source": "cache"}

    # Busca no banco se não tiver no redis
    usuarios_list = db.query(user.User).offset(offset).limit(limit).all()

    # Salva no Redis com  tempo  de vida (1 hora = 3600s)
    redis_client.set(key, str(usuarios_list), ex=3600)

    return {"data": str(usuarios_list), "source": "database"}
def count_usuarios(db: Session):
    return db.query(user.User).count()

# Buscar por ID no Redis
def get_usuario(db: Session, id: uuid.UUID):
    key = f"user:{id}"
    cached = redis_client.get(key)
    if cached:
        return {"data": cached, "source": "cache"}

    db_usuario = db.query(user.User).filter(user.User.id == id).first()
    if db_usuario:
        redis_client.set(key, str(db_usuario), ex=3600)
        return {"data": str(db_usuario), "source": "database"}

    return None

# Criar 
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

    redis_client.set(f"user:{novo_usuario.id}", str(novo_usuario), ex=3600)
    return novo_usuario

# Atualizar 
def update_usuario(db: Session, id: uuid.UUID, usuario: UserUpdate):
    db_usuario = db.query(user.User).filter(user.User.id == id).first()
    if not db_usuario:
        return None

    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)

    redis_client.set(f"user:{id}", str(db_usuario), ex=3600)
    return db_usuario

# Deletar 
def delete_usuario(db: Session, id: uuid.UUID):
    db_usuario = db.query(user.User).filter(user.User.id == id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        redis_client.delete(f"user:{id}")
        return True
    return False