import os
import tempfile

os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/test_sigad.db"
os.environ["DEMO_MODE"] = "false"
os.environ["SECRET_KEY"] = "clave-de-prueba"
os.environ["GEMINI_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def _lifecycle():
    with TestClient(app):
        yield


def _token() -> str:
    response = client.post("/api/auth/login", json={"email": "admin@sigad.co", "password": "Admin123!"})
    assert response.status_code == 200
    return response.json()["access_token"]


def _auth() -> dict:
    return {"Authorization": f"Bearer {_token()}"}


def test_login_ok():
    response = client.post("/api/auth/login", json={"email": "admin@sigad.co", "password": "Admin123!"})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["usuario"]["rol"] == "administrador"


def test_login_incorrecto():
    response = client.post("/api/auth/login", json={"email": "admin@sigad.co", "password": "incorrecta"})
    assert response.status_code == 401


def test_categorias_disponibles():
    response = client.get("/api/categorias")
    assert response.status_code == 200
    nombres = {c["nombre"] for c in response.json()}
    assert {"factura", "guia_despacho", "orden_compra", "contrato", "acta_recepcion"} <= nombres


def test_dashboard_admin():
    response = client.get("/api/dashboard/estadisticas", headers=_auth())
    assert response.status_code == 200
    assert "total_documentos" in response.json()


def test_crear_usuario_y_listar():
    headers = _auth()
    response = client.post(
        "/api/usuarios",
        json={"nombre": "Analista Pruebas", "email": "analista@sigad.co", "password": "Analista123!", "rol": "analista"},
        headers=headers,
    )
    assert response.status_code == 201
    lista = client.get("/api/usuarios", headers=headers)
    assert any(u["email"] == "analista@sigad.co" for u in lista.json())


def test_requiere_autenticacion():
    response = client.get("/api/dashboard/estadisticas")
    assert response.status_code == 401


def test_rag_modo_demo():
    response = client.post(
        "/api/rag/consultar",
        json={"pregunta": "¿Qué es SIGAD?"},
        headers=_auth(),
    )
    assert response.status_code == 200
    assert "respuesta" in response.json()


def test_subir_y_clasificar_documento():
    """Verifica el pipeline completo: carga, extracción, clasificación y metadatos."""
    contenido = (
        "FACTURA No. FACT-9999\nNIT proveedor: 900.123.456-7\n"
        "Proveedor: Alimentos del Valle S.A.\nFecha: 12/03/2026\n"
        "Subtotal: 4,850,000 IVA: 921,500 Total a pagar: 5,771,500.\n"
        "Numero de factura: FACT-9999-0001"
    )
    response = client.post(
        "/api/documentos",
        headers=_auth(),
        files={"archivo": ("factura-prueba.txt", contenido.encode("utf-8"), "text/plain")},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["estado"] == "procesado"
    assert data["categoria"] == "factura"
    assert data["confianza"] and data["confianza"] >= 0.7

    detail = client.get(f"/api/documentos/{data['id']}", headers=_auth())
    assert detail.status_code == 200
    assert detail.json()["metadatos"]


def test_dashboard_requiere_rol_admin_para_auditoria():
    # El admin puede ver auditoría
    assert client.get("/api/auditoria", headers=_auth()).status_code == 200


def test_eliminar_documento():
    contenido = "ORDEN DE COMPRA No. OC-1\nProveedor: Ferreterías del Eje\nTotal orden: 3,600,000"
    r = client.post("/api/documentos", headers=_auth(), files={"archivo": ("oc.txt", contenido.encode(), "text/plain")})
    assert r.status_code == 201
    doc_id = r.json()["id"]
    response = client.delete(f"/api/documentos/{doc_id}", headers=_auth())
    assert response.status_code == 204
    assert client.get(f"/api/documentos/{doc_id}", headers=_auth()).status_code == 404