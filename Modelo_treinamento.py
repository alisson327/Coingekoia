import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

from get_data_yahoo import get_data_yahoo  # usa seu script de coleta de dados do Yahoo

def gerar_targets(df, percentual=0.01):
    futuros = df["price"].shift(-15)  # Preço daqui 15 candles (~15 min)
    retorno_futuro = (futuros - df["price"]) / df["price"]

    condicoes = [
        (retorno_futuro > percentual),   # Sobe mais de 1%
        (retorno_futuro < -percentual),  # Cai mais de 1%
    ]
    escolhas = [2, 0]  # 2 = compra, 0 = venda
    df["target"] = np.select(condicoes, escolhas, default=1)  # 1 = manter

    return df.dropna()

def treinar_modelo():
    df = get_data_yahoo()
    if df.empty:
        print("⚠️ Erro: sem dados para treinar.")
        return

    df = gerar_targets(df)

    # Verifica se os dados possuem as colunas esperadas
    colunas = ["price", "sma_14", "rsi", "macd", "macd_signal", "boll_upper", "boll_lower", "boll_middle"]
    for col in colunas:
        if col not in df.columns:
            print(f"⚠️ Coluna ausente: {col}")
            return

    X = df[colunas]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(modelo, "modelo_classificador.pkl")
    print("✅ Modelo salvo como 'modelo_classificador.pkl'")

if __name__ == "__main__":
    treinar_modelo()
