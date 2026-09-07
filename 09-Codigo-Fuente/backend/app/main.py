from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, IS_POSTGRES, SessionLocal, engine, ensure_storage
from app.routes import (auditoria, auth, busqueda, categorias, dashboard,
                        documentos, rag, usuarios)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "API del Sistema Inteligente de Gestión y Análisis Documental. "
        "Flujo: archivo → extracción/OCR → procesamiento IA → clasificación → "
        "búsqueda semántica → consulta RAG."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for ruta in (auth.router, usuarios.router, categorias.router, documentos.router,
             busqueda.router, rag.router, dashboard.router, auditoria.router):
    app.include_router(ruta, prefix=settings.api_prefix)


@app.on_event("startup")
def _startup() -> None:
    from app import seed

    if not IS_POSTGRES:
        # Postgres en producción usa db/schema.sql (creación controlada).
        Base.metadata.create_all(bind=engine)
    ensure_storage()
    with SessionLocal() as db:
        seed.init_db(db)


@app.get("/")
def root():
    return {"app": settings.app_name, "docs": "/docs", "status": "ok"}