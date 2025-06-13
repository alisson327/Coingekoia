from get_data_fake import get_data_coingecko
from nucleo import gerar_sinal
from telegram_bot import enviar_sinal

if __name__ == "__main__":
    df = get_data_coingecko()
    if df.empty:
        print("⚠️ Nenhum dado retornado da fonte")
    else:
        sinal = gerar_sinal(df)
        if sinal:
            enviar_sinal(sinal)
