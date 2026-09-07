import json

import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.ia.engine import cosine_similarity, generar_respuesta, get_embedding
from app.models import Chunk, Consulta, Documento, Usuario
from app.schemas import FuenteOut, RagIn, RagOut

router = APIRouter(prefix="/rag", tags=["rag"])

TOP_K = 5


def _recuperar(pregunta: str, db: Session, limite: int = TOP_K) -> list[dict]:
    query_vector = np.asarray(get_embedding(pregunta).astype(float))
    candidatos: list[dict] = []
    chunks = (
        db.query(Chunk).join(Documento)
        .filter(Documento.estado == "procesado", Chunk.activo.is_(True))
        .all()
    )
    for chunk in chunks:
        if not chunk.embedding:
            continue
        try:
            vector = np.asarray(json.loads(chunk.embedding), dtype=float)
        except (ValueError, TypeError):
            continue
        puntaje = cosine_similarity(query_vector, vector)
        if puntaje <= 0.05:
            continue
        candidatos.append(
            {
                "documento_id": chunk.documento_id,
                "documento": chunk.documento.nombre_archivo,
                "fragmento": chunk.contenido[:600],
                "pagina": None,
                "puntaje": float(puntaje),
            }
        )
    candidatos.sort(key=lambda c: c["puntaje"], reverse=True)
    return candidatos[:limite]


@router.post("/consultar", response_model=RagOut)
def consultar(
    body: RagIn,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    recuperados = _recuperar(body.pregunta, db)
    respuesta = generar_respuesta(body.pregunta, recuperados)
    db.add(Consulta(usuario_id=usuario.id, pregunta=body.pregunta, respuesta=respuesta))
    db.commit()
    fuentes = [FuenteOut(**{k: v for k, v in f.items() if k != "puntaje"}) for f in recuperados]
    return RagOut(respuesta=respuesta, fuentes=fuentes)