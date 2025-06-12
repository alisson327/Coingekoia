from core import get_data_coingecko, gerar_sinal
from telegram_bot import enviar_sinal

if __name__ == "__main__":
    df = get_data_coingecko()
    if df.empty:
        print("⚠️ Nenhum dado retornado da CoinGecko")
    else:
        sinal = gerar_sinal(df)
        if sinal:
            enviar_sinal(sinal)
