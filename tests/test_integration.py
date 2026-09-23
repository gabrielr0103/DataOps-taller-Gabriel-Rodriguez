"""
Prueba de integración: ejecuta el mini-pipeline completo y valida el resultado final.
"""
from src.extract import extract_data
from src.transform import clean_data, calculate_metrics, aggregate_sales

DB_PATH = "data/ventas.db"


def test_pipeline_extraer_transformar_agregar():
    df = extract_data(DB_PATH)
    df = clean_data(df)
    df = calculate_metrics(df)
    resultado = aggregate_sales(df)

    assert not resultado.empty
    assert set(resultado.columns) == {"categoria", "mes", "venta_total"}
    