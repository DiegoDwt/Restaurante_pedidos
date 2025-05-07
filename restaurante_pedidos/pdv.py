import time
import requests
from models import StatusPedido

API_URL = "http://127.0.0.1:8000"

def buscar_pedidos_prontos():
    response = requests.get(f"{API_URL}/pedidos/pendentes/")
    if response.status_code == 200:
        pedidos = response.json()
        return [p for p in pedidos if p["status"] == StatusPedido.pronto]
    return []

def atualizar_status(pedido_id, novo_status):
    response = requests.put(
        f"{API_URL}/pedidos/{pedido_id}/status/",
        params={"novo_status": novo_status}
    )
    return response.ok

def finalizar_pedido(pedido):
    print(f"\n🧾 Entregando pedido para {pedido['cliente']}:")
    
    for item in pedido["itens"]:
        print(f"  🍔 {item['quantidade']}x {item['hamburguer']}")
    
    for bebida in pedido["bebidas"]:
        print(f"  🥤 {bebida['quantidade']}x {bebida['bebida']}")
    
    time.sleep(2)  # Simula tempo de atendimento
    atualizar_status(pedido["id"], StatusPedido.finalizado)
    print(f"🎉 Pedido {pedido['id']} finalizado!\n")

def loop_pdv():
    print("PDV iniciado. Aguardando pedidos prontos...")
    while True:
        pedidos = buscar_pedidos_prontos()
        for pedido in pedidos:
            finalizar_pedido(pedido)
        time.sleep(2)

if __name__ == "__main__":
    loop_pdv()
