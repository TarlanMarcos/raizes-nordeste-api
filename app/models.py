from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Loja(Base):
    __tablename__ = "lojas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    tipo_cozinha = Column(String)

    produtos = relationship("Produto", back_populates="loja")


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    sazonal = Column(Boolean, default=False)
    loja_id = Column(Integer, ForeignKey("lojas.id"))

    loja = relationship("Loja", back_populates="produtos")


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    canal_pedido = Column(String, nullable=False)  # APP, TOTEM, BALCAO, PICKUP, WEB
    status = Column(String, default="AGUARDANDO_PAGAMENTO")
    pagamento_status = Column(String, default="PENDENTE")  # PENDENTE, APROVADO, NEGADO
    valor_total = Column(Float, default=0.0)
    data_hora = Column(DateTime, default=datetime.now)
    loja_id = Column(Integer, ForeignKey("lojas.id"))

    loja = relationship("Loja")