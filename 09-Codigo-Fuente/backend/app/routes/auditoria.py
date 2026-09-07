from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_admin
from app.core.security import to_iso
from app.models import Auditoria
from app.schemas import AuditoriaOut

router = APIRouter(prefix="/auditoria", tags=["auditoria"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[AuditoriaOut])
def listar_auditoria(
    accion: str | None = None,
    limite: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(Auditoria)
    if accion:
        query = query.filter(Auditoria.accion == accion)
    registros = query.order_by(Auditoria.id.desc()).limit(limite).all()
    return [
        AuditoriaOut(
            id=r.id,
            usuario=r.usuario.nombre if r.usuario else None,
            accion=r.accion,
            detalle=r.detalle,
            ip=r.ip,
            creado_en=to_iso(r.creado_en),
        )
        for r in registros
    ]