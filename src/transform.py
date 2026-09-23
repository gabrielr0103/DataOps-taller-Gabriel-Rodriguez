"""
Módulo de transformación de datos.
Limpia los datos extraídos y calcula métricas de negocio.
"""
import pandas as pd


def clean_data(df):
    """
    - Elimina duplicados (comparando todas las columnas excepto `id`).
    - Rellena `cantidad` nulos con 0.
    - Rellena `precio_unitario` nulos con la media de la columna.
    - Convierte `fecha` a tipo datetime.
    """
    df = df.copy()

    columnas_negocio = [c for c in df.columns if c != "id"]
    df = df.drop_duplicates(subset=columnas_negocio, keep="first")

    df["cantidad"] = df["cantidad"].fillna(0)
    df["precio_unitario"] = df["precio_unitario"].fillna(df["precio_unitario"].mean())
    df["fecha"] = pd.to_datetime(df["fecha"])

    return df


def calculate_metrics(df):
    """
    Agrega columnas calculadas:
    - venta_total = cantidad * precio_unitario
    - mes = mes extraído de fecha
    """
    df = df.copy()
    df["venta_total"] = df["cantidad"] * df["precio_unitario"]
    df["mes"] = df["fecha"].dt.month
    return df


def aggregate_sales(df):
    """Agrupa las ventas por categoría y mes, sumando venta_total."""
    return df.groupby(["categoria", "mes"])["venta_total"].sum().reset_index()