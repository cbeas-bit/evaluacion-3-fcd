import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

print("Conectando a base de datos...")
conn = sqlite3.connect("uf.db")

df = pd.read_sql_query("SELECT * FROM uf ORDER BY periodo", conn)
conn.close()

print("Primeras filas:")
print(df.head())

df["periodo"] = pd.to_datetime(df["periodo"])
df["uf"] = pd.to_numeric(df["uf"], errors="coerce")
df.dropna(inplace=True)

df.set_index("periodo", inplace=True)

if len(df) < 60:
    print("ERROR: No hay suficientes datos para entrenar el LSTM.")
    exit()

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df[["uf"]])

def crear_dataset(data, steps=60):
    X, y = [], []
    for i in range(steps, len(data)):
        X.append(data[i-steps:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)

X, y = crear_dataset(scaled_data)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))



print("Creando modelo LSTM...")
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')
print(model.summary())
print("Entrenando modelo...")
history = model.fit(X, y, batch_size=32, epochs=20)
model.save("modelo_uf.keras")
print("Modelo guardado como modelo_uf.keras ")


ultimo_bloque = scaled_data[-60:]
ultimo_bloque = np.reshape(ultimo_bloque, (1, 60, 1))

pred_scaled = model.predict(ultimo_bloque)
pred = scaler.inverse_transform(pred_scaled)

print("\n Predicción UF para el día siguiente:", pred[0][0])
plt.figure(figsize=(10,5))
plt.plot(df.index[-300:], df["uf"].values[-300:], label="UF real")
plt.title("UF últimos 300 días")
plt.legend()
plt.show()
