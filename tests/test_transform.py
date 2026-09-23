"""
Pruebas unitarias para el módulo transform.
"""
import pandas as pd
import pytest

from src.transform import clean_data, calculate_metrics, aggregate_sales


@pytest.fixture
def df_ventas_crudo():
    """DataFrame de ejemplo con duplicados y nulos, simulando datos crudos."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4],
        "fecha": ["2026-01-10", "2026-01-10", "2026-02-05", "2026-02-05"],
        "producto": ["Mouse", "Mouse", "Camiseta", "Camiseta"],
        "categoria": ["Electronica", "Electronica", "Ropa", "Ropa"],
        "cantidad": [2, 2, None, 3],
        "precio_unitario": [50000.0, 50000.0, 30000.0, None],
        "cliente_id": [1001, 1001, 1002, 1002],
    })


def test_clean_data_elimina_duplicados(df_ventas_crudo):
    resultado = clean_data(df_ventas_crudo)
    # Las filas 1 y 2 son duplicados de negocio (mismos datos, id distinto)
    assert len(resultado) == 3


def test_clean_data_rellena_nulos(df_ventas_crudo):
    resultado = clean_data(df_ventas_crudo)
    assert resultado["cantidad"].isnull().sum() == 0
    assert resultado["precio_unitario"].isnull().sum() == 0

    fila_cantidad_nula = resultado[resultado["id"] == 3]
    assert fila_cantidad_nula["cantidad"].iloc[0] == 0


def test_calculate_metrics_venta_total(df_ventas_crudo):
    df = clean_data(df_ventas_crudo)
    df = calculate_metrics(df)
    for _, fila in df.iterrows():
        assert fila["venta_total"] == fila["cantidad"] * fila["precio_unitario"]


def test_aggregate_sales_agrupa_por_categoria_y_mes(df_ventas_crudo):
    df = clean_data(df_ventas_crudo)
    df = calculate_metrics(df)
    resultado = aggregate_sales(df)

    assert set(resultado.columns) == {"categoria", "mes", "venta_total"}
    # La suma agregada debe coincidir con la suma detallada (no se pierde dinero al agrupar)
    assert abs(resultado["venta_total"].sum() - df["venta_total"].sum()) < 1e-6
