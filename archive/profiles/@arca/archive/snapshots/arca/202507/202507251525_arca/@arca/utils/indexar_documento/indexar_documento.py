# utils/indexar_documento.py

import sqlite3
from pathlib import Path
from utils.load_config.load_config import load_config
from utils.load_schema.load_schema import load_schema

def indexar_documento(metadata: dict):
    """
    Inserta o actualiza un documento en el índice (tabla documentos),
    basado en el schema frontmatter.sql.yaml.
    """
    config = load_config()
    schemas = load_schema()
    db_path = Path(config["paths"]["base"]) / config["database"]["sqlite_path"]
    table = schemas["frontmatter_sql"]["table"]

    keys = metadata.keys()
    placeholders = ", ".join("?" for _ in keys)
    columns = ", ".join(keys)

    query = f"REPLACE INTO {table} ({columns}) VALUES ({placeholders})"

    conn = sqlite3.connect(db_path)
    conn.execute(query, tuple(metadata.values()))
    conn.commit()
    conn.close()
