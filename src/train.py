"""
Módulo de entrenamiento del modelo.
Entrena una regresión lineal simple para predecir ventas totales
en función del mes.
"""

import os

import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from src.extract import extract_data
from src.transform import clean_data, calculate_metrics, aggregate_sales


def train_model(df):
    """
    Entrena una regresión lineal usando `mes` (X) y `venta_total` (y).
    Recibe el resultado de aggregate_sales.

    Returns
    -------
    tuple
        (modelo entrenado, valor de R²)
    """
    X = df[["mes"]]
    y = df["venta_total"]

    modelo = LinearRegression()
    modelo.fit(X, y)
    r2 = r2_score(y, modelo.predict(X))

    os.makedirs("models", exist_ok=True)
    joblib.dump(modelo, os.path.join("models", "model.pkl"))

    return modelo, r2


def main():
    """Ejecuta el pipeline completo y entrena el modelo (usado por el CI)."""
    df = extract_data("data/ventas.db")
    df = clean_data(df)
    df = calculate_metrics(df)
    agg = aggregate_sales(df)

    _, r2 = train_model(agg)
    print(f"Modelo entrenado y guardado en models/model.pkl. R²: {r2:.4f}")


if __name__ == "__main__":
    main()
