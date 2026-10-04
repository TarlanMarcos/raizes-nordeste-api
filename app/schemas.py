from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---------- Loja ----------
class LojaBase(BaseModel):
    nome: str
    endereco: str
    tipo_cozinha: Optional[str] = None


class LojaCreate(LojaBase):
    pass


class LojaResponse(LojaBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Produto ----------
class ProdutoBase(BaseModel):
    nome: str
    preco: float
    sazonal: bool = False
    loja_id: int


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Pedido ----------
class PedidoBase(BaseModel):
    canal_pedido: str
    loja_id: int


class PedidoCreate(PedidoBase):
    pass


class PedidoResponse(PedidoBase):
    id: int
    status: str
    pagamento_status: str
    valor_total: float
    data_hora: datetime

    class Config:
        from_attributes = True


# ---------- Pagamento ----------
class PagamentoRequest(BaseModel):
    valor: float
    metodo: str = "MOCK"


class PagamentoResponse(BaseModel):
    pedido_id: int
    status_pagamento: str
    status_pedido: str
    mensagem: str