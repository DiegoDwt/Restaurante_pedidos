import time
import requests
from models import StatusPedido

API_URL = "http://127.0.0.1:8000"

def buscar_pedidos_recebidos():
    response = requests.get(f"{API_URL}/pedidos/pendentes/")
    if response.status_code == 200:
        pedidos = response.json()
        return [p for p in pedidos if p["status"] == StatusPedido.recebido]
    return []

def atualizar_status(pedido_id, novo_status):
    response = requests.put(
        f"{API_URL}/pedidos/{pedido_id}/status/",
        params={"novo_status": novo_status}
    )
    return response.ok

def preparar_pedido(pedido):
    print(f"\n🧑‍🍳 Preparo de pedido para {pedido['cliente']}:")
    
    for item in pedido["itens"]:
        print(f"  🍔 {item['quantidade']}x {item['hamburguer']}")
    
    for bebida in pedido["bebidas"]:
        print(f"  🥤 {bebida['quantidade']}x {bebida['bebida']}")
    
    atualizar_status(pedido["id"], StatusPedido.em_preparo)
    time.sleep(5)  # Simula tempo de preparo
    atualizar_status(pedido["id"], StatusPedido.pronto)
    print(f"✅ Pedido {pedido['id']} pronto!\n")

def loop_cozinha():
    print("Cozinha iniciada. Aguardando pedidos...")
    while True:
        pedidos = buscar_pedidos_recebidos()
        for pedido in pedidos:
            preparar_pedido(pedido)
        time.sleep(2)

if __name__ == "__main__":
    loop_cozinha()
