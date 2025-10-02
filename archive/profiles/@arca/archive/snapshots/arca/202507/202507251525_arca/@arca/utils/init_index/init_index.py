# utils/init_index.py

import sqlite3
from pathlib import Path
from utils.load_config.load_config import load_config
from utils.load_schema.load_schema import load_schema

def init_index():
    config = load_config()
    schemas = load_schema()
    db_path = Path(config["paths"]["base"]) / config["database"]["sqlite_path"]

    # Crea todas las tablas SQL encontradas en los schemas
    for schema_name, schema_sql in schemas.items():
        if schema_name.endswith("_sql"):
            table = schema_sql["table"]
            columns = schema_sql["columns"]
            col_defs = ",\n  ".join(f"{col['name']} {col['type']}" for col in columns)
            query = f"CREATE TABLE IF NOT EXISTS {table} (\n  {col_defs}\n)"
            conn = sqlite3.connect(db_path)
            conn.execute(query)
            conn.commit()
            conn.close()

