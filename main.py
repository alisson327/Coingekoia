from nucleo import get_data_yahoo, gerar_sinal
from telegram_bot import enviar_sinal

if __name__ == "__main__":
    df = get_data_yahoo()
    if df.empty:
        print("⚠️ Nenhum dado retornado")
    else:
        sinal = gerar_sinal(df)
        if sinal:
            enviar_sinal(sinal)
