import yfinance as yf import pandas
as pd from ta.momentum import 
RSIIndicator import MACD
def get_data_yahoo(): try: # Obtem os dados do BTC em 1m via Yahoo Finance df = yf.download(tickers='BTC-USD', interval='1m', period='1d')

if df.empty:
        print("⚠️ Nenhum dado retornado do Yahoo Finance")
        return pd.DataFrame()

    df = df.rename(columns={"Close": "price"})
    df = df.tail(50)  # Últimos 50 candles
    return df

except Exception as e:
    print("⚠️ Erro ao buscar dados do Yahoo Finance:", e)
    return pd.DataFrame()

def gerar_sinal(df): if df.empty: return None

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

