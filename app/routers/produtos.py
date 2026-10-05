from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app import models, schemas
from app.auth import exigir_perfil

router = APIRouter(prefix="/produtos", tags=["Produtos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=schemas.ProdutoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_produto(
    produto: schemas.ProdutoCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_perfil("ADMIN", "GERENTE"))
):
    """Cria um novo produto. Requer perfil ADMIN ou GERENTE."""
    loja = db.query(models.Loja).filter(models.Loja.id == produto.loja_id).first()
    if not loja:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada."
        )

    novo_produto = models.Produto(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@router.get("/", response_model=List[schemas.ProdutoResponse])
def listar_produtos(loja_id: int = None, db: Session = Depends(get_db)):
    """Lista produtos. Público."""
    query = db.query(models.Produto)
    if loja_id:
        query = query.filter(models.Produto.loja_id == loja_id)
    return query.all()