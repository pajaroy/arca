# utils/logger.py

from loguru import logger
from pathlib import Path
from datetime import datetime
import sqlite3

from utils.hash_utils.hash_utils import hash_string
from utils.uuid_utils.uuid_utils import generar_uuid
from utils.load_config.load_config import load_config
from utils.load_schema.load_schema import load_schema

# Cargar configuración
config = load_config()
schemas = load_schema()

base_path = Path(config["paths"]["base"])
log_level = config["logs"].get("level", "INFO").upper()
destino = config["logs"].get("destino", "db").lower()
table = config["logs"].get("table", "logs")
db_path = Path(config["paths"]["base"]) / config["database"]["sqlite_path"]

# Inicializar log a archivo si aplica
if destino in ("file", "ambos"):
    log_file = base_path / f"{table}.log"
    logger.remove()
    logger.add(
        str(log_file),
        rotation="10 MB",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {message}"
    )

def log_event(level: str, module: str, message: str, accion: str = "evento"):
    """
    Registra un evento en log (archivo y/o base de datos) según configuración.
    """
    timestamp = datetime.now().isoformat()
    uuid_val = generar_uuid()
    hash_val = hash_string(f"{timestamp}|{level}|{module}|{accion}|{message}")
    nivel = level.upper()

    # Loguear en archivo
    if destino in ("file", "ambos"):
        getattr(logger, level.lower())(f"[{module}] {message}")

    # Loguear en base de datos
    if destino in ("db", "ambos"):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO {table} (
                uuid, timestamp, nivel, modulo, accion, detalle, hash_integridad
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            uuid_val,
            timestamp,
            nivel,
            module,
            accion,
            message,
            hash_val
        ))
        conn.commit()
        conn.close()
