
import requests

TOKEN = "7769222423:AAEdsNAgBpk4lg9NTsuiT4qt_pY6FXIDiOE"
CHAT_ID = "7841170326"

def enviar_sinal(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": mensagem}
        requests.post(url, data=data)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
