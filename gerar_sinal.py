def gerar_sinal(df):
    ultima_linha = df.iloc[-1]

    rsi = ultima_linha['rsi']
    macd = ultima_linha['macd']
    macd_signal = ultima_linha['macd_signal']
    close = ultima_linha['price']
    atr = df['price'].rolling(window=14).std().iloc[-1] * 2  # proxy do ATR

    resistencia = df['price'].rolling(window=20).max().iloc[-2]
    suporte = df['price'].rolling(window=20).min().iloc[-2]

    direcao = None
    if rsi < 30 and macd > macd_signal:
        direcao = 'compra'
    elif rsi > 70 and macd < macd_signal:
        direcao = 'venda'

    if not direcao:
        return None

    if direcao == 'compra':
        stop_loss = round(close - atr, 2)
        take_profit = round(close + (resistencia - close) * 0.9, 2)
    else:
        stop_loss = round(close + atr, 2)
        take_profit = round(close - (close - suporte) * 0.9, 2)

    mensagem = (
        f"🔔 Sinal de {direcao.upper()}\n"
        f"📈 Preço: {round(close, 2)}\n"
        f"🎯 Take Profit: {take_profit}\n"
        f"🛑 Stop Loss: {stop_loss}\n"
        f"📊 RSI: {round(rsi, 2)} | MACD: {round(macd, 2)}\n"
    )
    return mensagem
