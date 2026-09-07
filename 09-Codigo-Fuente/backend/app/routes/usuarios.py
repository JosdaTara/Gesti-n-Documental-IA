from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_admin
from app.core.security import hash_password, to_iso
from app.models import Usuario
from app.schemas import UsuarioIn, UsuarioOut, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["usuarios"], dependencies=[Depends(require_admin)])


def _serializar(u: Usuario) -> UsuarioOut:
    return UsuarioOut(
        id=u.id,
        nombre=u.nombre,
        email=u.email,
        rol=u.rol,
        activo=u.activo,
        creado_en=to_iso(u.creado_en),
        ultimo_acceso=to_iso(u.ultimo_acceso),
    )


@router.get("", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return [_serializar(u) for u in db.query(Usuario).order_by(Usuario.id).all()]


@router.post("", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(body: UsuarioIn, db: Session = Depends(get_db)):
    email = body.email.lower()
    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, detail="El correo ya está registrado")
    usuario = Usuario(
        nombre=body.nombre,
        email=email,
        password_hash=hash_password(body.password),
        rol=body.rol,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return _serializar(usuario)


@router.put("/{usuario_id}", response_model=UsuarioOut)
def actualizar_usuario(usuario_id: int, body: UsuarioUpdate, db: Session = Depends(get_db)):
    if body.password is None and body.nombre is None and body.rol is None and body.activo is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Sin cambios enviados")
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    if body.nombre is not None:
        usuario.nombre = body.nombre
    if body.rol is not None:
        usuario.rol = body.rol
    if body.password is not None:
        usuario.password_hash = hash_password(body.password)
    db.commit()
    db.refresh(usuario)
    return _serializar(usuario)