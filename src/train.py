"""
Módulo de entrenamiento del modelo.
Entrena una regresión lineal simple para predecir ventas totales
en función del mes.
"""
import os

import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def train_model(df):
    X = df[["mes"]]
    y = df["venta_total"]

    modelo = LinearRegression()
    modelo.fit(X, y)
    r2 = r2_score(y, modelo.predict(X))

    os.makedirs("models", exist_ok=True)
    joblib.dump(modelo, os.path.join("models", "model.pkl"))

    return modelo, r2
