import mimetypes
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import Chunk, Documento, Usuario
from app.schemas import ClasificacionIn, DocumentoDetail, DocumentoOut, EstadoDocumento
from app.services import documento_detail, documento_out, procesar_documento, reasignar_categoria, registrar_auditoria

router = APIRouter(prefix="/documentos", tags=["documentos"])

EXTENSIONES_PERMITIDAS = {".pdf", ".docx", ".txt", ".md", ".jpg", ".jpeg", ".png"}
TAMANIO_MAX = 15 * 1024 * 1024


def _ruta_destino(nombre_archivo: str, estado: str) -> tuple[Path, str]:
    carpeta = Path(settings.storage_path)
    if estado:
        carpeta = carpeta / estado
    carpeta.mkdir(parents=True, exist_ok=True)
    ext = Path(nombre_archivo).suffix.lower()
    destino = carpeta / f"{uuid.uuid4().hex}{ext}"
    return destino, str(destino)


@router.post("", response_model=DocumentoOut, status_code=status.HTTP_201_CREATED)
async def subir_documento(
    request: Request,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    nombre = Path(archivo.filename or "documento").name
    ext = Path(nombre).suffix.lower()
    if ext not in EXTENSIONES_PERMITIDAS:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Formato no permitido. Use PDF, DOCX, TXT, MD, JPG o PNG",
        )
    contenido = await archivo.read()
    if len(contenido) > TAMANIO_MAX:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="El archivo supera los 15 MB")
    mime = mimetypes.guess_type(nombre)[0] or "application/octet-stream"

    destino, ruta = _ruta_destino(nombre, "pendiente")
    destino.write_bytes(contenido)

    documento = Documento(
        nombre_archivo=nombre,
        ruta_archivo=ruta,
        tipo_mime=mime,
        tamano_bytes=len(contenido),
        estado="pendiente",
        cargado_por=usuario.id,
    )
    db.add(documento)
    db.commit()
    db.refresh(documento)

    try:
        procesar_documento(db, documento)
    except Exception as exc:  # noqa: BLE001
        documento.estado = "rechazado"
        db.commit()
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"No se pudo procesar el documento: {exc}",
        ) from exc

    registrar_auditoria(db, usuario.id, "documento.cargar", nombre, request.client.host if request.client else None)
    db.refresh(documento)
    return documento_out(documento)


@router.get("", response_model=list[DocumentoOut])
def listar_documentos(
    estado: EstadoDocumento | None = None,
    categoria: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Documento)
    if estado:
        query = query.filter(Documento.estado == estado)
    if categoria:
        query = query.filter(Documento.categoria.has(nombre=categoria.lower()))
    if q:
        like = f"%{q.lower()}%"
        query = query.filter(Documento.nombre_archivo.ilike(like))
    return [documento_out(d) for d in query.order_by(Documento.id.desc()).all()]


@router.get("/{documento_id}", response_model=DocumentoDetail)
def detalle_documento(documento_id: int, db: Session = Depends(get_db)):
    documento = db.get(Documento, documento_id)
    if documento is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")
    return documento_detail(documento)


@router.get("/{documento_id}/archivo")
def descargar_documento(documento_id: int, db: Session = Depends(get_db)):
    documento = db.get(Documento, documento_id)
    if documento is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")
    ruta = Path(documento.ruta_archivo)
    if not ruta.exists():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Archivo físico no disponible")
    return FileResponse(ruta, filename=documento.nombre_archivo)


@router.put("/{documento_id}/clasificacion", response_model=DocumentoOut)
def reclasificar(
    documento_id: int,
    body: ClasificacionIn,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    documento = db.get(Documento, documento_id)
    if documento is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")
    reasignar_categoria(db, documento, body.categoria_id)
    registrar_auditoria(
        db, usuario.id, "documento.clasificar", f"{documento.nombre_archivo} -> categoria {body.categoria_id}",
        request.client.host if request.client else None,
    )
    db.refresh(documento)
    return documento_out(documento)


@router.delete("/{documento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_documento(
    documento_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    documento = db.get(Documento, documento_id)
    if documento is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")
    ruta = Path(documento.ruta_archivo)
    if ruta.exists():
        ruta.unlink()
    db.delete(documento)
    db.commit()
    registrar_auditoria(db, usuario.id, "documento.eliminar", documento.nombre_archivo,
                        request.client.host if request.client else None)