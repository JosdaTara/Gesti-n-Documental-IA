from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import Categoria, Consulta, Documento
from app.schemas import EstadisticasOut

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/estadisticas", response_model=EstadisticasOut, dependencies=[Depends(get_current_user)])
def estadisticas(db: Session = Depends(get_db)):
    total = db.query(func.count(Documento.id)).scalar() or 0
    procesados = (
        db.query(func.count(Documento.id)).filter(Documento.estado == "procesado").scalar() or 0
    )
    pendientes = (
        db.query(func.count(Documento.id)).filter(Documento.estado.in_(["pendiente", "en_proceso"])).scalar() or 0
    )
    revision = (
        db.query(func.count(Documento.id)).filter(Documento.estado == "requiere_revision").scalar() or 0
    )
    consultas = db.query(func.count(Consulta.id)).scalar() or 0

    por_categoria = []
    for categoria in db.query(Categoria).filter(Categoria.activa.is_(True)).order_by(Categoria.id).all():
        cantidad = (
            db.query(func.count(Documento.id))
            .filter(Documento.categoria_id == categoria.id, Documento.estado == "procesado")
            .scalar()
            or 0
        )
        por_categoria.append({"categoria": categoria.nombre, "cantidad": cantidad})

    estados_nombres = ["procesado", "requiere_revision", "pendiente", "en_proceso", "rechazado"]
    por_estado = []
    for estado in estados_nombres:
        cantidad = db.query(func.count(Documento.id)).filter(Documento.estado == estado).scalar() or 0
        por_estado.append({"estado": estado, "cantidad": cantidad})

    hoy = datetime.utcnow()
    inicio = hoy - timedelta(days=6)
    por_semana = []
    for dia in range(7):
        fecha = (inicio + timedelta(days=dia)).date()
        desde = datetime(fecha.year, fecha.month, fecha.day)
        hasta = desde + timedelta(days=1)
        cantidad = (
            db.query(func.count(Documento.id))
            .filter(Documento.cargado_en >= desde, Documento.cargado_en < hasta)
            .scalar()
            or 0
        )
        por_semana.append({"fecha": fecha.isoformat(), "cantidad": cantidad})

    return EstadisticasOut(
        total_documentos=total,
        total_procesados=procesados,
        pendientes=pendientes,
        revision=revision,
        total_consultas=consultas,
        por_categoria=por_categoria,
        por_estado=por_estado,
        por_semana=por_semana,
    )