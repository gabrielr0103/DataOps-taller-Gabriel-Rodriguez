import os


def save_to_csv(df, path):
    """Guarda un DataFrame en CSV, creando la carpeta destino si no existe."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
