# tests/test_flujo_creacion.py

from utils.init_index.init_index import init_index
from core.cmd.crear.crear_archivo import crear_archivo
from utils.load_config.load_config import load_config
import sqlite3
from pathlib import Path

def test_crear_archivo_y_validar_trazabilidad():
    config = load_config()
    base = Path(config["paths"]["base"])
    db_path = base / config["database"]["sqlite_path"]
    data_dir = base / config["paths"]["data"]

    # Inicializar tabla
    init_index()

    # Crear archivo de prueba
    nombre = "archivo_test"
    tipo = "txt"
    contenido = "Contenido de prueba"
    autor = "test_user"
    path_archivo = crear_archivo(nombre, contenido, tipo, autor)

    # Verificar archivo creado
    assert path_archivo.exists(), "El archivo no fue creado"

    # Verificar que el documento fue indexado
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documentos WHERE nombre = ?", (nombre,))
    resultado = cursor.fetchone()
    assert resultado is not None, "El documento no fue indexado en la base de datos"
    conn.close()

    print("[TEST PASADO] Archivo creado, indexado y registrado correctamente.")
