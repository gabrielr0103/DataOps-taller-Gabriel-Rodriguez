"""
Script de creación de la base de datos SQLite para el proyecto.
Genera la tabla ventas con datos simulados, incluyendo algunos
valores nulos y duplicados para las pruebas de calidad de datos.
"""
import os
import random
import sqlite3
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ventas.db")

PRODUCTOS = {
    "Electronica": ["Audifonos", "Cargador", "Mouse", "Teclado"],
    "Ropa": ["Camiseta", "Pantalon", "Chaqueta", "Medias"],
    "Hogar": ["Lampara", "Cortina", "Cojin", "Vela"],
    "Deportes": ["Balon", "Pesas", "Colchoneta", "Guantes"],}


def crear_tabla(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY,
            fecha TEXT,
            producto TEXT,
            categoria TEXT,
            cantidad INTEGER,
            precio_unitario REAL,
            cliente_id INTEGER
        )
    """)


def generar_registros(n=120):
    fecha_inicio = datetime(2026, 1, 1)
    base_registros = []

    for _ in range(n):
        categoria = random.choice(list(PRODUCTOS.keys()))
        producto = random.choice(PRODUCTOS[categoria])
        fecha = (fecha_inicio + timedelta(days=random.randint(0, 240))).strftime("%Y-%m-%d")
        cantidad = random.randint(1, 10)
        precio_unitario = round(random.uniform(5000, 250000), 2)
        cliente_id = random.randint(1000, 1050)

        # Nulos a propósito, para las pruebas de calidad de datos
        if random.random() < 0.05:
            cantidad = None
        if random.random() < 0.05:
            precio_unitario = None

        base_registros.append((fecha, producto, categoria, cantidad, precio_unitario, cliente_id))

    # Duplicados "de negocio" (mismos datos, id distinto), para probar drop_duplicates
    base_registros += random.sample(base_registros, 5)

    return [(i + 1, *r) for i, r in enumerate(base_registros)]


def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)  # permite re-ejecutar el script sin errores

    conn = sqlite3.connect(DB_PATH)
    crear_tabla(conn)
    registros = generar_registros(120)
    conn.executemany(
        "INSERT INTO ventas (id, fecha, producto, categoria, cantidad, precio_unitario, cliente_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        registros,
    )
    conn.commit()
    conn.close()
    print(f"Base de datos creada en {DB_PATH} con {len(registros)} registros.")


if __name__ == "__main__":
    main()

