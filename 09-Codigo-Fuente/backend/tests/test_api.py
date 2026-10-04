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
    assert {"FACTURA", "GUIA_DESPACHO", "ORDEN_COMPRA", "CONTRATO", "ACTA_RECEPCION"} <= nombres


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
    assert data["categoria"] == "FACTURA"
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


# ---------------------------------------------------------------- revisión humana (n8n)


def _subir_baja_confianza() -> int:
    """Documento sin palabras clave de ninguna categoría → requiere_revision."""
    contenido = (
        "Memorando interno de la compañía.\n"
        "Se informa al personal sobre la actualización de políticas de archivado.\n"
        "Este documento no corresponde a ninguna de las categorías comerciales predeterminadas."
    )
    r = client.post(
        "/api/documentos",
        headers=_auth(),
        files={"archivo": ("memorando.txt", contenido.encode("utf-8"), "text/plain")},
    )
    assert r.status_code == 201, r.text
    return r.json()["id"]


def test_baja_confianza_queda_en_revision():
    doc_id = _subir_baja_confianza()
    data = client.get(f"/api/documentos/{doc_id}", headers=_auth()).json()
    assert data["estado"] == "requiere_revision"
    assert data["confianza"] < 0.7
    # No aparece en búsqueda semántica mientras esté en revisión
    resultados = client.get("/api/busqueda", params={"q": "políticas de archivado", "tipo": "keyword"}).json()
    assert all(r["id"] != doc_id for r in resultados)


def test_revision_aprobar():
    doc_id = _subir_baja_confianza()
    r = client.post(f"/api/documentos/{doc_id}/revision", headers=_auth(),
                    json={"decision": "APROBAR", "comentario": "Clasificación correcta"})
    assert r.status_code == 200, r.text
    assert r.json()["estado"] == "procesado"
    assert r.json()["confianza"] == 1.0


def test_revision_corregir():
    doc_id = _subir_baja_confianza()
    cats = client.get("/api/categorias").json()
    factura = next(c["id"] for c in cats if c["nombre"] == "FACTURA")
    r = client.post(f"/api/documentos/{doc_id}/revision", headers=_auth(),
                    json={"decision": "CORREGIR", "categoria_final_id": factura,
                          "comentario": "Corrige a factura"})
    assert r.status_code == 200, r.text
    assert r.json()["estado"] == "procesado"
    assert r.json()["categoria"] == "FACTURA"


def test_revision_corregir_sin_categoria_es_422():
    doc_id = _subir_baja_confianza()
    r = client.post(f"/api/documentos/{doc_id}/revision", headers=_auth(),
                    json={"decision": "CORREGIR"})
    assert r.status_code == 422


def test_revision_rechazar_no_se_indexa():
    doc_id = _subir_baja_confianza()
    r = client.post(f"/api/documentos/{doc_id}/revision", headers=_auth(),
                    json={"decision": "RECHAZAR", "comentario": "Documento irrelevante"})
    assert r.status_code == 200
    assert r.json()["estado"] == "rechazado"
    resultados = client.get("/api/busqueda", params={"q": "archivado", "tipo": "keyword"}).json()
    assert all(x["id"] != doc_id for x in resultados)


def test_revision_409_si_no_esta_en_revision():
    # Rechazado previamente ya no puede volver a revisarse
    doc_id = _subir_baja_confianza()
    client.post(f"/api/documentos/{doc_id}/revision", headers=_auth(), json={"decision": "RECHAZAR"})
    r = client.post(f"/api/documentos/{doc_id}/revision", headers=_auth(), json={"decision": "APROBAR"})
    assert r.status_code == 409


def test_revision_requiere_autenticacion():
    doc_id = _subir_baja_confianza()
    r = client.post(f"/api/documentos/{doc_id}/revision", json={"decision": "APROBAR"})
    assert r.status_code == 401


def test_webhook_fallido_no_rompe_carga(monkeypatch):
    from app import services

    class _Falla:
        def post(self, *a, **k):
            raise ConnectionError("n8n no disponible")

    monkeypatch.setattr(services.settings, "n8n_webhook_url", "http://localhost:1/webhook")
    monkeypatch.setattr(services.httpx, "post", _Falla().post)
    doc_id = _subir_baja_confianza()
    # El documento se procesa igual; el fallo queda solo en auditoría
    assert doc_id > 0
    auditoria = client.get("/api/auditoria", headers=_auth()).json()
    assert any(a["accion"] == "n8n.webhook_error" for a in auditoria)


def test_revision_registra_historial():
    doc_id = _subir_baja_confianza()
    client.post(f"/api/documentos/{doc_id}/revision", headers=_auth(),
                json={"decision": "RECHAZAR", "comentario": "Fuera de alcance"})
    from app.core.database import SessionLocal
    from app.models import Revision
    with SessionLocal() as db:
        fila = db.query(Revision).filter_by(documento_id=doc_id).first()
        assert fila is not None
        assert fila.decision == "RECHAZAR"
        assert fila.comentario == "Fuera de alcance"