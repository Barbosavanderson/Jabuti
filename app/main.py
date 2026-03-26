from fastapi import FastAPI
from app.api import usuarios, test_redis
from app.db.session import Base, engine
from app.models import user  # noqa: F401 - ensure model metadata is registered


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Desafio Jabuti - CRUD de Usuários",
    version="1.0.0",
    description="API para gerenciar usuários com FastAPI, PostgreSQL e Redis"
)

app.include_router(usuarios.router, tags=["usuarios"])

app.include_router(test_redis.router)