from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import create_access_token, to_iso, verify_password
from app.models import Usuario
from app.schemas import LoginIn, TokenOut, UsuarioOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == body.email.lower()).first()
    if usuario is None or not verify_password(body.password, usuario.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    if not usuario.activo:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")
    from datetime import datetime

    usuario.ultimo_acceso = datetime.utcnow()
    db.commit()
    token = create_access_token(str(usuario.id))
    return TokenOut(
        access_token=token,
        usuario=UsuarioOut(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            rol=usuario.rol,
            activo=usuario.activo,
            creado_en=to_iso(usuario.creado_en),
            ultimo_acceso=to_iso(usuario.ultimo_acceso),
        ),
    )


@router.get("/me", response_model=UsuarioOut)
def me(usuario: Usuario = Depends(get_current_user)):
    return UsuarioOut(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        rol=usuario.rol,
        activo=usuario.activo,
        creado_en=to_iso(usuario.creado_en),
        ultimo_acceso=None,
    )