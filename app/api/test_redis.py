from fastapi import APIRouter
from app.db.redis_config import redis_client

router = APIRouter()

@router.get("/redis-test")
def redis_test():
    try:
        redis_client.set("teste_api", "conectado")
        valor = redis_client.get("teste_api")
        return {"status": "Conectado esta Blackezera.", "valor": valor}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}