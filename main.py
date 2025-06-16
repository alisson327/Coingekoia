from nucleo import get_data_yahoo, gerar_sinal
from telegram_bot import enviar_sinal

if __name__ == "__main__":
    df = get_data_yahoo()
    if df.empty:
        print("⚠️ Nenhum dado retornado")
    else:
        sinal = gerar_sinal(df)
        if sinal:
            # Informações fictícias por enquanto
            entrada = df["price"].iloc[-1]
            tp1 = round(entrada * 1.002, 4)
            tp2 = round(entrada * 1.004, 4)
            tp3 = round(entrada * 1.007, 4)
            tp4 = round(entrada * 1.013, 4)
            sl = round(entrada * 0.99, 4)

            porcentagens = {
                "tp1": 77,
                "tp2": 55,
                "tp3": 30,
                "tp4": 10
            }

            mensagem = f"""📈 BTC/USDT • {'LONG' if 'alta' in sinal else 'SHORT'} • Alav. 20x
• Entrada: {entrada:.2f}
• TP1: {tp1} ({porcentagens['tp1']}%) / TP2: {tp2} ({porcentagens['tp2']}%) / TP3: {tp3} ({porcentagens['tp3']}%) / TP4: {tp4} ({porcentagens['tp4']}%)
• SL: {sl}
• Stop móvel: Ativa após TP1
"""

            enviar_sinal(mensagem)
