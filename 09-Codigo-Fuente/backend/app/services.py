from datetime import datetime

import httpx
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import ensure_storage
from app.core.security import to_iso
from app.ia import engine
from app.models import Auditoria, Categoria, MetadatoDocumento, Chunk, Documento, Revision, Usuario


def registrar_auditoria(db: Session, usuario_id: int | None, accion: str, detalle: str | None, ip: str | None = None) -> None:
    db.add(Auditoria(usuario_id=usuario_id, accion=accion, detalle=detalle, ip=ip))
    db.commit()


def _notificar_n8n(payload: dict) -> bool:
    """POST fire-and-forget al webhook de n8n. Nunca rompe el flujo del documento.

    Devuelve True si se entregó (o no había webhook configurado). Si falla,
    deja registro en auditoria; los reintentos los asume n8n de forma reactiva.
    """
    if not settings.n8n_webhook_url:
        return True
    try:
        httpx.post(settings.n8n_webhook_url, json=payload, timeout=8.0)
        return True
    except Exception:  # noqa: BLE001
        return False


def _notificar_revision_abierta(db: Session, documento: Documento, categoria_nombre: str | None) -> None:
    payload = {
        "evento": "revision_abierta",
        "documento_id": documento.id,
        "documento": documento.nombre_archivo,
        "categoria_sugerida": categoria_nombre,
        "confianza": documento.confianza,
        "resumen": documento.resumen,
        "url_revision": f"{settings.frontend_url}/app/revision",
    }
    ok = _notificar_n8n(payload)
    accion = "n8n.revision_abierta" if ok else "n8n.webhook_error"
    registrar_auditoria(db, None, accion, documento.nombre_archivo)


def procesar_documento(db: Session, documento: Documento) -> None:
    """Pipeline: extracción → chunks → embeddings → clasificación → metadatos → resumen."""
    documento.estado = "en_proceso"
    db.commit()

    texto = engine.extract_text(documento.ruta_archivo, documento.tipo_mime)
    documento.texto_extraido = texto

    categoria_key, confianza = engine.clasificar(texto)
    categoria = None
    if categoria_key:
        categoria = (
            db.query(Categoria)
            .filter(func.lower(Categoria.nombre) == categoria_key, Categoria.activa.is_(True))
            .first()
        )
    documento.categoria_id = categoria.id if categoria else None
    documento.confianza = confianza
    # En modo demo, siempre enviamos a revisión humana para facilitar pruebas E2E
    if settings.demo_mode and categoria:
        documento.confianza = min(confianza, 0.62)
        documento.estado = "requiere_revision"
    else:
        documento.estado = "procesado" if (categoria and confianza >= 0.70) else "requiere_revision"
    documento.resumen = engine.resumir(texto)
    documento.procesado_en = datetime.utcnow()

    for chunk in documento.chunks:
        db.delete(chunk)
    db.flush()

    for indice, contenido in enumerate(engine.chunk_text(texto)):
        db.add(
            Chunk(
                documento_id=documento.id,
                indice=indice,
                contenido=contenido[:1800],
                embedding=engine.embed_json(contenido[:1200]),
            )
        )

    for metadato in documento.metadatos:
        db.delete(metadato)
    db.flush()
    for clave, valor in engine.extract_metadatos(texto).items():
        db.add(MetadatoDocumento(documento_id=documento.id, clave=clave, valor=valor))

    db.commit()

    if documento.estado == "requiere_revision":
        _notificar_revision_abierta(db, documento, categoria.nombre if categoria else None)


def revisar_documento(db: Session, documento: Documento, body, usuario: Usuario) -> dict:
    """Aplica la decisión humana sobre un documento en requiere_revision.

    - APROBAR: conserva la categoría sugerida y pasa a procesado.
    - CORREGIR: asigna categoria_final_id al documento y pasa a procesado.
    - RECHAZAR: deja el documento en rechazado (no se indexa).
    Registra auditoria, guarda el historial en `revisiones` y notifica a n8n.
    """
    if body.decision == "CORREGIR" and body.categoria_final_id is None:
        raise ValueError("CORREGIR requiere categoria_final_id")

    db.add(
        Revision(
            documento_id=documento.id,
            categoria_sugerida=documento.categoria.nombre if documento.categoria else None,
            confianza=documento.confianza,
            decision=body.decision,
            categoria_final_id=body.categoria_final_id,
            comentario=body.comentario or None,
            revisado_por=usuario.id,
        )
    )

    if body.decision == "APROBAR":
        documento.estado = "procesado"
        documento.confianza = 1.0
        accion = "documento.aprobar"
    elif body.decision == "CORREGIR":
        documento.categoria_id = body.categoria_final_id
        documento.estado = "procesado"
        documento.confianza = 1.0
        accion = "documento.corregir"
    else:
        documento.estado = "rechazado"
        accion = "documento.rechazar"

    db.commit()

    registrar_auditoria(db, usuario.id, accion, f"{documento.nombre_archivo} -> {documento.estado}")

    if settings.n8n_webhook_url:
        ok = _notificar_n8n(
            {
                "evento": "revision_cerrada",
                "documento_id": documento.id,
                "documento": documento.nombre_archivo,
                "decision": body.decision,
                "estado": documento.estado,
                "categoria_final": documento.categoria.nombre if documento.categoria else None,
                "url_revision": f"{settings.frontend_url}/app/revision",
            }
        )
        registrar_auditoria(db, usuario.id, "n8n.revision_cerrada" if ok else "n8n.webhook_error",
                            documento.nombre_archivo)

    db.refresh(documento)
    return documento_out(documento)


def reasignar_categoria(db: Session, documento: Documento, categoria_id: int) -> None:
    documento.categoria_id = categoria_id
    documento.confianza = 1.0
    documento.estado = "procesado"
    db.commit()


# ---------------------------------------------------------------- serializers
def documento_out(doc: Documento) -> dict:
    return {
        "id": doc.id,
        "nombre_archivo": doc.nombre_archivo,
        "tipo_mime": doc.tipo_mime,
        "tamano_bytes": doc.tamano_bytes,
        "estado": doc.estado,
        "categoria": doc.categoria.nombre if doc.categoria else None,
        "confianza": doc.confianza,
        "resumen": doc.resumen,
        "cargado_en": to_iso(doc.cargado_en),
        "procesado_en": to_iso(doc.procesado_en),
    }


def documento_detail(doc: Documento) -> dict:
    out = documento_out(doc)
    out["metadatos"] = [{"clave": m.clave, "valor": m.valor} for m in doc.metadatos]
    return out