from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app import models, schemas
from app.auth import get_usuario_atual

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=schemas.PedidoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_pedido(
    pedido: schemas.PedidoCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_usuario_atual)
):
    """Cria um novo pedido. Requer autenticação."""
    loja = db.query(models.Loja).filter(models.Loja.id == pedido.loja_id).first()
    if not loja:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada."
        )

    canais_validos = ["APP", "TOTEM", "BALCAO", "PICKUP", "WEB"]
    if pedido.canal_pedido not in canais_validos:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Canal inválido. Use um dos: {canais_validos}"
        )

    novo_pedido = models.Pedido(
        canal_pedido=pedido.canal_pedido,
        loja_id=pedido.loja_id,
        status="AGUARDANDO_PAGAMENTO",
        pagamento_status="PENDENTE"
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido


@router.get("/", response_model=List[schemas.PedidoResponse])
def listar_pedidos(
    canal_pedido: str = None,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_usuario_atual)
):
    """Lista pedidos. Requer autenticação."""
    query = db.query(models.Pedido)
    if canal_pedido:
        query = query.filter(models.Pedido.canal_pedido == canal_pedido)
    return query.all()


@router.get("/{pedido_id}", response_model=schemas.PedidoResponse)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_usuario_atual)
):
    """Busca um pedido pelo ID. Requer autenticação."""
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado."
        )
    return pedido