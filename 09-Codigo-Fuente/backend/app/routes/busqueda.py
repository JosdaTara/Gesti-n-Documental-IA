import json

import numpy as np
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.ia.engine import cosine_similarity, get_embedding
from app.models import Chunk, Documento
from app.schemas import BusquedaOut

router = APIRouter(prefix="/busqueda", tags=["busqueda"])


@router.get("", response_model=list[BusquedaOut])
def buscar(
    q: str = Query(min_length=2, max_length=200),
    tipo: str = Query("semantica", pattern="^(keyword|semantica)$"),
    categoria: str | None = None,
    limite: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(Chunk).join(Documento).filter(
        Documento.estado == "procesado", Chunk.activo.is_(True)
    )
    if categoria:
        query = query.filter(Documento.categoria.has(nombre=categoria.lower()))

    if tipo == "keyword":
        return _buscar_keyword(query, q, limite)

    query_embedding = np.asarray(get_embedding(q).astype(float))
    resultados = []
    for chunk in query.all():
        if not chunk.embedding:
            continue
        try:
            chunk_vector = np.asarray(json.loads(chunk.embedding), dtype=float)
        except (ValueError, TypeError):
            continue
        puntaje = cosine_similarity(query_embedding, chunk_vector)
        if puntaje <= 0.05:
            continue
        resultados.append(
            {
                "id": chunk.documento_id,
                "documento": chunk.documento.nombre_archivo,
                "estado": chunk.documento.estado,
                "categoria": chunk.documento.categoria.nombre if chunk.documento.categoria else None,
                "fragmento": chunk.contenido[:280],
                "puntaje": round(float(puntaje), 3),
                "confianza": chunk.documento.confianza,
            }
        )
    resultados.sort(key=lambda r: r["puntaje"], reverse=True)
    return resultados[:limite]


def _buscar_keyword(query, q: str, limite: int) -> list[dict]:
    termino = q.lower()
    resultados = []
    for chunk in query.all():
        contenido = chunk.contenido.lower()
        posicion = contenido.find(termino)
        if posicion >= 0:
            inicio = max(0, posicion - 120)
            fragmento = chunk.contenido[inicio : posicion + 240].strip()
            resultados.append(
                {
                    "id": chunk.documento_id,
                    "documento": chunk.documento.nombre_archivo,
                    "estado": chunk.documento.estado,
                    "categoria": chunk.documento.categoria.nombre if chunk.documento.categoria else None,
                    "fragmento": fragmento,
                    "puntaje": round(min(1.0, 0.4 + 0.2 * (len(termino) / max(len(termino), 1))), 3),
                    "confianza": chunk.documento.confianza,
                }
            )
    return resultados[:limite]