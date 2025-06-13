import requests
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

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
        prices = data["prices"][-50:]  # 50 candles para RSI/MACD

        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except Exception as e:
        print("⚠️ Erro ao buscar dados da CoinGecko:", e)
        return pd.DataFrame()

def gerar_sinal(df):
    if df.empty:
        return None

    df["rsi"] = RSIIndicator(df["price"]).rsi()
    macd = MACD(df["price"])
    df["macd"] = macd.macd()
    df["signal"] = macd.macd_signal()

    # Regras básicas de sinal
    rsi = df["rsi"].iloc[-1]
    macd_line = df["macd"].iloc[-1]
    signal_line = df["signal"].iloc[-1]

    if rsi > 70 and macd_line < signal_line:
        return "📉 Sinal de baixa BTC (15m)"
    elif rsi < 30 and macd_line > signal_line:
        return "📈 Sinal de alta BTC (15m)"
    else:
        return None
