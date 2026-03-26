import uuid
from fastapi.testclient import TestClient

from app.main import app
from app.crud import usuarios as usuarios_crud


client = TestClient(app)


def test_list_usuarios_ok(monkeypatch):
    payload = [
        {
            "id": str(uuid.uuid4()),
            "nome": "Ana",
            "email": "ana@example.com",
            "idade": 25,
        }
    ]

    def fake_get_usuarios(db, limit=10, offset=0):  # noqa: ARG001
        return payload

    monkeypatch.setattr(usuarios_crud, "get_usuarios", fake_get_usuarios)
    response = client.get("/usuarios/?limit=10&offset=0")

    assert response.status_code == 200
    assert response.json() == payload


def test_read_usuario_invalid_uuid_returns_400():
    response = client.get("/usuarios/not-a-uuid")
    assert response.status_code == 400
    assert response.json()["detail"] == "UUID inválido"


def test_read_usuario_not_found_returns_404(monkeypatch):
    def fake_get_usuario(db, id):  # noqa: ARG001
        return None

    monkeypatch.setattr(usuarios_crud, "get_usuario", fake_get_usuario)
    response = client.get(f"/usuarios/{uuid.uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"


def test_create_usuario_ok(monkeypatch):
    created = {
        "id": str(uuid.uuid4()),
        "nome": "Bruno",
        "email": "bruno@example.com",
        "idade": 30,
    }

    def fake_create_usuario(db, usuario):  # noqa: ARG001
        return created

    monkeypatch.setattr(usuarios_crud, "create_usuario", fake_create_usuario)

    response = client.post(
        "/usuarios/",
        json={"nome": "Bruno", "email": "bruno@example.com", "idade": 30},
    )

    assert response.status_code == 200
    assert response.json() == created


def test_update_usuario_not_found_returns_404(monkeypatch):
    def fake_update_usuario(db, id, usuario):  # noqa: ARG001
        return None

    monkeypatch.setattr(usuarios_crud, "update_usuario", fake_update_usuario)
    response = client.put(
        f"/usuarios/{uuid.uuid4()}",
        json={"nome": "Novo Nome"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"


def test_delete_usuario_ok(monkeypatch):
    def fake_delete_usuario(db, id):  # noqa: ARG001
        return True

    monkeypatch.setattr(usuarios_crud, "delete_usuario", fake_delete_usuario)
    response = client.delete(f"/usuarios/{uuid.uuid4()}")

    assert response.status_code == 200
    assert response.json() == {"status": "deletado"}
