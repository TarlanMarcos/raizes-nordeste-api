from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import lojas, produtos, pedidos, pagamentos, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Raízes do Nordeste", version="1.0.0")

app.include_router(auth.router)
app.include_router(lojas.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)


@app.get("/", tags=["Raiz"])
def raiz():
    return {"mensagem": "API Raízes do Nordeste rodando!"}