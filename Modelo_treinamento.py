import pandas as pd import numpy as np from sklearn.ensemble import RandomForestClassifier from sklearn.model_selection import train_test_split from sklearn.metrics import classification_report import joblib

from get_data_coingecko import get_data_coingecko

def gerar_targets(df, percentual=0.01): futuros = df["price"].shift(-15)  # preço daqui 15 minutos retorno_futuro = (futuros - df["price"]) / df["price"]

condicoes = [
    (retorno_futuro > percentual),   # subir mais que 1% 
    (retorno_futuro < -percentual),  # cair mais que 1%
]
escolhas = [2, 0]  # 2 = comprar, 0 = vender
df["target"] = np.select(condicoes, escolhas, default=1)  # 1 = manter
return df.dropna()

def treinar_modelo(): df = get_data_coingecko() if df.empty: print("Erro: sem dados para treinar.") return

df = gerar_targets(df)

# Features
X = df[["price", "sma_14", "rsi", "macd", "macd_signal", "boll_upper", "boll_lower", "boll_middle"]]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(modelo, "modelo_classificador.pkl")
print("✅ Modelo salvo como 'modelo_classificador.pkl'")

if name == "main": treinar_modelo()

