import os
import shutil
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ventas.db")
SNAPSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "snapshots")


def create_snapshot():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"No se encontró la base de datos en: {DB_PATH}")

    os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
    fecha = datetime.now().strftime("%Y%m%d")
    destino = os.path.join(SNAPSHOTS_DIR, f"ventas_{fecha}.db")
    shutil.copy2(DB_PATH, destino)
    print(f"Snapshot creado: {destino}")
    return destino


if __name__ == "__main__":
    create_snapshot()