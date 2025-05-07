from enum import Enum
from pydantic import BaseModel, Field
from typing import List
from uuid import UUID, uuid4

# Status do pedido
class StatusPedido(str, Enum):
    recebido = "recebido"
    em_preparo = "em_preparo"
    pronto = "pronto"
    finalizado = "finalizado"

# Tipos de bebidas disponíveis
class Bebida(str, Enum):
    agua = "agua"
    refrigerante = "refrigerante"
    cerveja = "cerveja"

# Tipos de hambúrgueres disponíveis
class Hamburguer(str, Enum):
    x_burguer = "X-Burguer"
    x_salada = "X-Salada"
    x_bacon = "X-Bacon"
    x_egg = "X-Egg"
    x_tudo = "X-Tudo"
    x_frango = "X-Frango"
    vegetariano = "Vegetariano"
    vegano = "Vegano"
    duplo_burguer = "Duplo Burguer"
    artesanal = "Artesanal"

# Modelo de um item do pedido (hambúrguer)
class ItemPedido(BaseModel):
    hamburguer: Hamburguer
    quantidade: int = Field(gt=0, description="Quantidade de hambúrguer deve ser > 0")

# Modelo para a bebida no pedido
class BebidaPedido(BaseModel):
    bebida: Bebida
    quantidade: int = Field(gt=0, description="Quantidade de bebida deve ser > 0")

# Modelo do Pedido, com o UUID do pedido gerado automaticamente
class Pedido(BaseModel):
    id: UUID
    cliente: str
    itens: List[ItemPedido]
    bebidas: List[BebidaPedido]
    status: StatusPedido

    @staticmethod
    def criar(cliente: str, itens: List[ItemPedido], bebidas: List[BebidaPedido]) -> "Pedido":
        return Pedido(
            id=uuid4(),
            cliente=cliente,
            itens=itens,
            bebidas=bebidas,
            status=StatusPedido.recebido
        )
