"""
Módulo de extracción de datos.
Lee la tabla ventas desde la base de datos SQLite y la retorna
como un DataFrame de pandas.
"""
import os
import sqlite3

import pandas as pd


def extract_data(db_path):
    """
    Extrae todos los registros de la tabla `ventas`.

    Parameters
    ----------
    db_path : str
        Ruta al archivo de la base de datos SQLite.

    Returns
    -------
    pandas.DataFrame

    Raises
    ------
    FileNotFoundError
        Si el archivo de la base de datos no existe.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"No se encontró la base de datos en: {db_path}")

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM ventas", conn)
    finally:
        conn.close()

    return df