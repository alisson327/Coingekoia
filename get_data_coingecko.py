import requests
import pandas as pd
import numpy as np

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

        # Extrair os últimos 100 candles (mais dados para cálculo de indicadores)
        prices = data["prices"][-100:]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        # Indicadores
        df["returns"] = df["price"].pct_change()

        # Média Móvel Simples de 14 períodos
        df["sma_14"] = df["price"].rolling(window=14).mean()

        # RSI
        delta = df["price"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df["rsi"] = 100 - (100 / (1 + rs))

        # MACD
        ema_12 = df["price"].ewm(span=12, adjust=False).mean()
        ema_26 = df["price"].ewm(span=26, adjust=False).mean()
        df["macd"] = ema_12 - ema_26
        df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

        # Bollinger Bands (20 períodos, 2 desvios)
        sma_20 = df["price"].rolling(window=20).mean()
        std_20 = df["price"].rolling(window=20).std()
        df["boll_upper"] = sma_20 + (2 * std_20)
        df["boll_lower"] = sma_20 - (2 * std_20)
        df["boll_middle"] = sma_20

        # Remover valores NaN
        df.dropna(inplace=True)

        return df

    except Exception as e:
        print("⚠️ Erro ao buscar dados da CoinGecko:", e)
        return pd.DataFrame()
