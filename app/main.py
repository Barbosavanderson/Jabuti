from fastapi import FastAPI
from app.api import usuarios
from app.db.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Desafio Jabuti - CRUD de Usuários",
    version="1.0.0",
    description="API para gerenciar usuários com FastAPI, PostgreSQL e Redis"
)

app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])