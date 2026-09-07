from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


EmbeddingType = Text().with_variant(MEDIUMTEXT, "mysql")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), nullable=False, default="analista")  # administrador | analista
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    ultimo_acceso: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    auditorias: Mapped[list["Auditoria"]] = relationship(back_populates="usuario")


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(200), default="")
    activa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Documento(Base):
    __tablename__ = "documentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_archivo: Mapped[str] = mapped_column(String(255), nullable=False)
    ruta_archivo: Mapped[str] = mapped_column(String(500), nullable=False)
    tipo_mime: Mapped[str] = mapped_column(String(120), nullable=False, default="application/octet-stream")
    tamano_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estado: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pendiente", index=True
    )  # pendiente | en_proceso | procesado | requiere_revision | rechazado
    categoria_id: Mapped[int | None] = mapped_column(ForeignKey("categorias.id"), nullable=True)
    confianza: Mapped[float | None] = mapped_column(Float, nullable=True)
    resumen: Mapped[str | None] = mapped_column(Text, nullable=True)
    texto_extraido: Mapped[str | None] = mapped_column(Text, nullable=True)
    cargado_por: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    cargado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    procesado_en: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    categoria: Mapped[Categoria | None] = relationship()
    metadatos: Mapped[list["MetadatoDocumento"]] = relationship(
        back_populates="documento", cascade="all, delete-orphan"
    )
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="documento", cascade="all, delete-orphan")


class MetadatoDocumento(Base):
    __tablename__ = "metadatos_documento"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documentos.id", ondelete="CASCADE"), index=True)
    clave: Mapped[str] = mapped_column(String(60), nullable=False)
    valor: Mapped[str] = mapped_column(String(300), nullable=False)

    documento: Mapped[Documento] = relationship(back_populates="metadatos")


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documentos.id", ondelete="CASCADE"), index=True)
    indice: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[str] = mapped_column(EmbeddingType, nullable=True)  # vector JSON (MEDIUMTEXT en MySQL)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    documento: Mapped[Documento] = relationship(back_populates="chunks")


class Auditoria(Base):
    __tablename__ = "auditoria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    accion: Mapped[str] = mapped_column(String(60), nullable=False)
    detalle: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip: Mapped[str | None] = mapped_column(String(60), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    usuario: Mapped[Usuario | None] = relationship(back_populates="auditorias")


class Consulta(Base):
    __tablename__ = "consultas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    pregunta: Mapped[str] = mapped_column(Text, nullable=False)
    respuesta: Mapped[str] = mapped_column(Text, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())