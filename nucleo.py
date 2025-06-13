import requests
import pandas as pd

def get_data_coingecko():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "interval": "minutely"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        print(data)  # debug

        # Extrair os últimos 15 candles
        prices = data["prices"][-15:]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df

    except Exception as e:
        print("⚠️ Erro ao buscar dados da CoinGecko:", e)
        return pd.DataFrame()

def gerar_sinal(df):
    if df.empty:
        return None

    df["media"] = df["price"].rolling(window=5).mean()

    if df["price"].iloc[-1] > df["media"].iloc[-1]:
        return "📈 Sinal de alta BTC (15m)"
    elif df["price"].iloc[-1] < df["media"].iloc[-1]:
        return "📉 Sinal de baixa BTC (15m)"
    else:
        return None
