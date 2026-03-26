from sqlalchemy.orm import Session
from app.models import user
from app.schemas.user import UserCreate, UserUpdate
from app.db.redis_config import redis_client
import json
import uuid

_CACHE_ENABLED = True


def _cache_get(key: str):
    global _CACHE_ENABLED
    if not _CACHE_ENABLED:
        return None
    try:
        return redis_client.get(key)
    except Exception:
        _CACHE_ENABLED = False
        return None


def _cache_set(key: str, value: dict, ttl_seconds: int = 3600):
    global _CACHE_ENABLED
    if not _CACHE_ENABLED:
        return
    try:
        redis_client.set(key, json.dumps(value), ex=ttl_seconds)
    except Exception:
        _CACHE_ENABLED = False


def _cache_delete(key: str):
    global _CACHE_ENABLED
    if not _CACHE_ENABLED:
        return
    try:
        redis_client.delete(key)
    except Exception:
        _CACHE_ENABLED = False

# Paginação segura
def get_usuarios(db: Session, limit: int = 10, offset: int = 0):
    if limit < 1:
        limit = 10
    if offset < 0:
        offset = 0
    return db.query(user.User).offset(offset).limit(limit).all()

def count_usuarios(db: Session):
    return db.query(user.User).count()

# Buscar por ID com cache Redis
def get_usuario(db: Session, id: uuid.UUID):
    key = f"user:{id}"
    cached = _cache_get(key)
    if cached:
        return json.loads(cached)

    db_usuario = db.query(user.User).filter(user.User.id == id).first()
    if db_usuario:
        payload = {
            "id": str(db_usuario.id),
            "nome": db_usuario.nome,
            "email": db_usuario.email,
            "idade": db_usuario.idade,
        }
        _cache_set(key, payload, ttl_seconds=3600)
        return payload

    return None

# Criar usuário
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

    payload = {
        "id": str(novo_usuario.id),
        "nome": novo_usuario.nome,
        "email": novo_usuario.email,
        "idade": novo_usuario.idade,
    }
    _cache_set(f"user:{novo_usuario.id}", payload, ttl_seconds=3600)
    return novo_usuario

# Atualizar usuário
def update_usuario(db: Session, id: uuid.UUID, usuario: UserUpdate):
    db_usuario = db.query(user.User).filter(user.User.id == id).first()
    if not db_usuario:
        return None

    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)

    payload = {
        "id": str(db_usuario.id),
        "nome": db_usuario.nome,
        "email": db_usuario.email,
        "idade": db_usuario.idade,
    }
    _cache_set(f"user:{id}", payload, ttl_seconds=3600)
    return db_usuario

# Deletar usuário
def delete_usuario(db: Session, id: uuid.UUID):
    db_usuario = db.query(user.User).filter(user.User.id == id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        _cache_delete(f"user:{id}")
        return True
    return False