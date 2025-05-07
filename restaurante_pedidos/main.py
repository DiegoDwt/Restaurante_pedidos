from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from uuid import UUID
from models import Pedido, StatusPedido, ItemPedido, BebidaPedido

app = FastAPI()

# Banco de dados em memória (simulado)
pedidos_db: List[Pedido] = []

# Modelo de entrada do pedido
class PedidoInput(BaseModel):
    cliente: str
    itens: List[ItemPedido]
    bebidas: List[BebidaPedido]

@app.post("/pedidos/", response_model=Pedido)
def criar_pedido(pedido_input: PedidoInput):
    pedido = Pedido.criar(
        cliente=pedido_input.cliente,
        itens=pedido_input.itens,
        bebidas=pedido_input.bebidas
    )
    pedidos_db.append(pedido)
    return pedido

@app.get("/pedidos/", response_model=List[Pedido])
def listar_pedidos():
    return pedidos_db

@app.get("/pedidos/pendentes/", response_model=List[Pedido])
def listar_pedidos_pendentes():
    return [p for p in pedidos_db if p.status != StatusPedido.finalizado]

@app.put("/pedidos/{pedido_id}/status/", response_model=Pedido)
def atualizar_status(pedido_id: UUID, novo_status: StatusPedido):
    for pedido in pedidos_db:
        if pedido.id == pedido_id:
            pedido.status = novo_status
            return pedido
    raise HTTPException(status_code=404, detail="Pedido não encontrado")

@app.get("/pedidos/{pedido_id}", response_model=Pedido)
def obter_pedido(pedido_id: UUID):
    for pedido in pedidos_db:
        if pedido.id == pedido_id:
            return pedido
    raise HTTPException(status_code=404, detail="Pedido não encontrado")
