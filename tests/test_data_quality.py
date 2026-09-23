"""
Pruebas de esquema y calidad de datos sobre la tabla `ventas`.
"""
import pandas as pd
import pytest

from src.extract import extract_data

DB_PATH = "data/ventas.db"

COLUMNAS_ESPERADAS = {
    "id", "fecha", "producto", "categoria",
    "cantidad", "precio_unitario", "cliente_id",
}


@pytest.fixture(scope="module")
def df_ventas():
    return extract_data(DB_PATH)


def test_tabla_tiene_columnas_esperadas(df_ventas):
    assert COLUMNAS_ESPERADAS.issubset(set(df_ventas.columns))


def test_cantidad_no_tiene_valores_negativos(df_ventas):
    cantidades = df_ventas["cantidad"].dropna()
    assert (cantidades >= 0).all()


def test_precio_unitario_es_mayor_que_cero(df_ventas):
    precios = df_ventas["precio_unitario"].dropna()
    assert (precios > 0).all()


def test_no_hay_fechas_futuras(df_ventas):
    fechas = pd.to_datetime(df_ventas["fecha"])
    hoy = pd.Timestamp.now().normalize()
    assert (fechas <= hoy).all()