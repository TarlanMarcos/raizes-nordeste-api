from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app import models, schemas
from app.auth import exigir_perfil

router = APIRouter(prefix="/lojas", tags=["Lojas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=schemas.LojaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_loja(
    loja: schemas.LojaCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_perfil("ADMIN", "GERENTE"))
):
    """Cria uma nova loja. Requer perfil ADMIN ou GERENTE."""
    nova_loja = models.Loja(**loja.dict())
    db.add(nova_loja)
    db.commit()
    db.refresh(nova_loja)
    return nova_loja


@router.get("/", response_model=List[schemas.LojaResponse])
def listar_lojas(db: Session = Depends(get_db)):
    """Lista todas as lojas. Público."""
    return db.query(models.Loja).all()