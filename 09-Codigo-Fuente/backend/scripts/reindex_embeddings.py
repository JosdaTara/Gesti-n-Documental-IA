"""Re-indexa los embeddings de todos los chunks usando el proveedor actualmente activo.

Necesario al cambiar de proveedor de embeddings (ej: de Gemini a OpenRouter),
porque los vectores quedan en un espacio semántico distinto y las búsquedas
semánticas anteriores dejan de ser comparables.

Uso (desde la carpeta backend/):
    python scripts/reindex_embeddings.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings
from app.core.database import SessionLocal
from app.ia import engine
from app.models import Chunk


def main() -> None:
    db = SessionLocal()
    try:
        total = 0
        for chunk in db.query(Chunk).all():
            contenido = (chunk.contenido or "")[:1200]
            if not contenido:
                continue
            chunk.embedding = engine.embed_json(contenido)
            total += 1
            if total % 10 == 0:
                db.commit()
                print(f"  ... {total} chunks reindexados")
        db.commit()
        if total == 0:
            print("No hay chunks que reindexar.")
            return
        proveedor = "OpenRouter" if settings.openrouter_api_key else "proveedor activo"
        print(f"Listo: {total} chunks reindexados con {proveedor}.")
    finally:
        db.close()


if __name__ == "__main__":
    main()