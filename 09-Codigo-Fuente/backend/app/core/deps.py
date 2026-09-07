from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models import Usuario


def get_current_user(
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None),
) -> Usuario:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token no proporcionado")
    payload = decode_access_token(authorization.split(" ", 1)[1].strip())
    if not payload or "sub" not in payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
    usuario = db.get(Usuario, int(payload["sub"]))
    if usuario is None or not usuario.activo:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado o inactivo")
    return usuario


def require_admin(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    if usuario.rol != "administrador":
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Requiere rol administrador")
    return usuario