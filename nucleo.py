import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

def get_data_yahoo():
    try:
        df = yf.download(tickers='BTC-USD', interval='1m', period='1d')
        df.reset_index(inplace=True)

        df["timestamp"] = pd.to_datetime(df["Datetime"])
        df["price"] = df["Close"]  # <- Aqui: agora "price" é uma Series
        df = df[["timestamp", "price"]]  # Mantém só o necessário
        return df

    except Exception as e:
        print("⚠️ Erro ao buscar dados do Yahoo Finance:", e)
        return pd.DataFrame()

def gerar_sinal(df):
    if df.empty:
        return None

    # Garantir que 'price' é Series
    price_series = df["price"]

    df["rsi"] = RSIIndicator(close=price_series).rsi()
    macd = MACD(close=price_series)
    df["macd"] = macd.macd()
    df["signal"] = macd.macd_signal()

    rsi = df["rsi"].iloc[-1]
    macd_line = df["macd"].iloc[-1]
    signal_line = df["signal"].iloc[-1]

    if rsi > 70 and macd_line < signal_line:
        return "📉 Sinal de baixa BTC (15m)"
    elif rsi < 30 and macd_line > signal_line:
        return "📈 Sinal de alta BTC (15m)"
    else:
        return None
