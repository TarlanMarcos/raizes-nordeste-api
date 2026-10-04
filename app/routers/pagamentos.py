from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{pedido_id}", response_model=schemas.PagamentoResponse)
def processar_pagamento(
    pedido_id: int,
    pagamento: schemas.PagamentoRequest,
    db: Session = Depends(get_db)
):
    """
    Simula o pagamento de um pedido.

    Regra do mock:
    - Se valor <= 100 → APROVADO
    - Se valor > 100  → NEGADO
    """
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado."
        )

    if pedido.status != "AGUARDANDO_PAGAMENTO":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Pedido já está com status {pedido.status}."
        )

    # Simulação do pagamento (mock)
    if pagamento.valor <= 100:
        pedido.pagamento_status = "APROVADO"
        pedido.status = "PAGO"
        mensagem = "Pagamento aprovado com sucesso."
    else:
        pedido.pagamento_status = "NEGADO"
        pedido.status = "CANCELADO"
        mensagem = "Pagamento negado pelo serviço externo."

    pedido.valor_total = pagamento.valor
    db.commit()
    db.refresh(pedido)

    return schemas.PagamentoResponse(
        pedido_id=pedido.id,
        status_pagamento=pedido.pagamento_status,
        status_pedido=pedido.status,
        mensagem=mensagem
    )