from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Rol = Literal["administrador", "analista"]
EstadoDocumento = Literal["pendiente", "en_proceso", "procesado", "requiere_revision", "rechazado"]


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: "UsuarioOut"


class UsuarioIn(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    rol: Rol = "analista"


class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    rol: Rol | None = None
    activo: bool | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: EmailStr
    rol: str
    activo: bool
    creado_en: str | None = None
    ultimo_acceso: str | None = None


class CategoriaIn(BaseModel):
    nombre: str = Field(min_length=2, max_length=60)
    descripcion: str = Field(default="", max_length=200)


class CategoriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str
    activa: bool


class MetadatoOut(BaseModel):
    clave: str
    valor: str


class DocumentoOut(BaseModel):
    id: int
    nombre_archivo: str
    tipo_mime: str
    tamano_bytes: int
    estado: str
    categoria: str | None = None
    confianza: float | None = None
    resumen: str | None = None
    cargado_en: str | None = None
    procesado_en: str | None = None


class DocumentoDetail(DocumentoOut):
    metadatos: list[MetadatoOut] = Field(default_factory=list)


class ClasificacionIn(BaseModel):
    categoria_id: int


class BusquedaOut(BaseModel):
    id: int
    documento: str
    estado: str
    categoria: str | None = None
    fragmento: str
    puntaje: float
    confianza: float | None = None


class RagIn(BaseModel):
    pregunta: str = Field(min_length=4, max_length=500)


class FuenteOut(BaseModel):
    documento_id: int
    documento: str
    fragmento: str
    pagina: int | None = None


class RagOut(BaseModel):
    respuesta: str
    fuentes: list[FuenteOut] = Field(default_factory=list)


class AuditoriaOut(BaseModel):
    id: int
    usuario: str | None = None
    accion: str
    detalle: str | None = None
    ip: str | None = None
    creado_en: str | None = None


class EstadisticasOut(BaseModel):
    total_documentos: int
    total_procesados: int
    pendientes: int
    revision: int
    total_consultas: int
    por_categoria: list[dict]
    por_estado: list[dict]
    por_semana: list[dict]


UsuarioOut.model_rebuild()
TokenOut.model_rebuild()