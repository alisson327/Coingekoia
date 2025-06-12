
import requests
import time
from telegram_bot import enviar_sinal

def obter_preco_coingecko(cripto='bitcoin', moeda='usd'):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={cripto}&vs_currencies={moeda}'
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        return dados[cripto][moeda]
    except Exception as e:
        print("Erro ao obter preço:", e)
        return None

def estrategia_simples(preco_atual):
    if preco_atual is None:
        return None
    # Exemplo fictício de lógica: se preço for múltiplo de 500, sinal de compra
    if int(preco_atual) % 500 < 10:
        return {
            'entrada': preco_atual,
            'take_profit': round(preco_atual * 1.02, 2),
            'stop_loss': round(preco_atual * 0.98, 2),
            'mensagem': f"SINAL BTC\nEntrada: {preco_atual}\nTP: {round(preco_atual * 1.02, 2)}\nSL: {round(preco_atual * 0.98, 2)}"
        }
    return None

if __name__ == "__main__":
    while True:
        preco = obter_preco_coingecko()
        sinal = estrategia_simples(preco)
        if sinal:
            enviar_sinal(sinal['mensagem'])
        time.sleep(900)  # 15 minutos
