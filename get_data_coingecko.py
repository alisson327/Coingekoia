import pandas as pd
import numpy as np

def get_data_coingecko():
    # Simula 100 candles com timestamps e preços
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=100, freq="15min")
    prices = np.linspace(67000, 66000, 100) + np.random.normal(0, 100, 100)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "price": prices
    })
    df.set_index("timestamp", inplace=True)

    # Simula os mesmos indicadores
    df["returns"] = df["price"].pct_change()
    df["sma_14"] = df["price"].rolling(window=14).mean()

    delta = df["price"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))

    ema_12 = df["price"].ewm(span=12, adjust=False).mean()
    ema_26 = df["price"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema_12 - ema_26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

    sma_20 = df["price"].rolling(window=20).mean()
    std_20 = df["price"].rolling(window=20).std()
    df["boll_upper"] = sma_20 + (2 * std_20)
    df["boll_lower"] = sma_20 - (2 * std_20)
    df["boll_middle"] = sma_20

    df.dropna(inplace=True)
    return df
