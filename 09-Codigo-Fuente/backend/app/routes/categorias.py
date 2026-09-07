from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_admin
from app.models import Categoria
from app.schemas import CategoriaOut

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return [c for c in db.query(Categoria).order_by(Categoria.id).all()]


@router.post("", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def crear_categoria(nombre: str, descripcion: str = "", db: Session = Depends(get_db)):
    nombre = nombre.strip().lower()
    if db.query(Categoria).filter(Categoria.nombre == nombre).first():
        raise HTTPException(status.HTTP_409_CONFLICT, detail="La categoría ya existe")
    categoria = Categoria(nombre=nombre, descripcion=descripcion)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria