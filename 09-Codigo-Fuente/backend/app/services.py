from datetime import datetime

from sqlalchemy.orm import Session

from app.core.database import ensure_storage
from app.core.security import to_iso
from app.ia import engine
from app.models import Auditoria, Categoria, MetadatoDocumento, Chunk, Documento


def registrar_auditoria(db: Session, usuario_id: int | None, accion: str, detalle: str | None, ip: str | None = None) -> None:
    db.add(Auditoria(usuario_id=usuario_id, accion=accion, detalle=detalle, ip=ip))
    db.commit()


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
            db.query(Categoria).filter(Categoria.nombre == categoria_key, Categoria.activa.is_(True)).first()
        )
    documento.categoria_id = categoria.id if categoria else None
    documento.confianza = confianza
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