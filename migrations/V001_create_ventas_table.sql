CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY,
    fecha TEXT,
    producto TEXT,
    categoria TEXT,
    cantidad INTEGER,
    precio_unitario REAL,
    cliente_id INTEGER
);