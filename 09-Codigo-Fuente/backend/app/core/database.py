from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _is_postgres(url: str) -> bool:
    return url.startswith("postgresql")


IS_POSTGRES = _is_postgres(settings.database_url)

if IS_POSTGRES:
    engine = create_engine(settings.database_url, pool_pre_ping=True, pool_size=10)
else:
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection, _record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_storage() -> None:
    Path(settings.storage_path).mkdir(parents=True, exist_ok=True)
    for sub in ("pendiente", "en_proceso", "factura", "guia_despacho", "orden_compra", "contrato", "acta_recepcion"):
        Path(settings.storage_path, sub).mkdir(parents=True, exist_ok=True)