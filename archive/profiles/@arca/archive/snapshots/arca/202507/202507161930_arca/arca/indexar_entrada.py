"""METADATOS\nuuid: 2b1fab81-2e15-4158-80ba-c18245e4fdad
tipo: py
nombre: indexador
version: 0.1.0
estado: activo
fecha_creacion: '2025-07-16T02:28:00.498860'
fecha_modificacion: '2025-07-16T02:28:00.498928'
autor: Bir
descripcion: Indexador universal
hash_integridad: 1377c2d5dab8bbbcc9215536e408f57239540936cfbc8dc159cbfa69f1155134
\n"""

from load_config import load_config
from datetime import datetime
from pathlib import Path
import yaml

CONFIG = load_config()
INDEX_PATH = Path(CONFIG["config"]["index_path"])
INDEX_STRUCT = CONFIG["config"]["index_estructura"]

def indexar_entrada(info):
    """
    Indexa archivos o directorios en el índice central.
    El dict 'info' debe tener, al menos: uuid, nombre, ruta, tipo.
    """
    # Cargar índice actual o inicializarlo vacío
    if INDEX_PATH.exists():
        with open(INDEX_PATH, "r") as f:
            index = yaml.safe_load(f) or []
    else:
        index = []

    # Evitar duplicados (por uuid)
    index = [x for x in index if x.get("uuid") != info.get("uuid")]

    # Armar estructura a partir de index_estructura (garantiza los campos)
    index_entry = dict(INDEX_STRUCT)
    index_entry.update(info)
    index_entry["indexado_en"] = datetime.now().isoformat()

    index.append(index_entry)

    # Guardar actualizado
    with open(INDEX_PATH, "w") as f:
        yaml.dump(index, f, sort_keys=False)

    print(f"Entrada indexada: {index_entry.get('tipo', '???')} - {index_entry.get('nombre', index_entry.get('ruta', ''))}")

# --------- USO DE EJEMPLO ---------
if __name__ == "__main__":
    # Ejemplo para un directorio
    indexar_entrada({
        "uuid": "dir-1234",
        "nombre": "dataset",
        "ruta": "datos/dataset",
        "tipo": "directorio",
        "hash_integridad": "",
        "fecha_creacion": datetime.now().isoformat(),
        "fecha_modificacion": datetime.now().isoformat(),
        "autor": "Bird",
        "descripcion": "Directorio de datos para pruebas",
    })

    # Ejemplo para un archivo
    indexar_entrada({
        "uuid": "file-9876",
        "nombre": "notebook",
        "ruta": "notebooks/prueba.ipynb",
        "tipo": "notebook",
        "hash_integridad": "abc123",
        "fecha_creacion": datetime.now().isoformat(),
        "fecha_modificacion": datetime.now().isoformat(),
        "autor": "Bird",
        "descripcion": "Notebook de ejemplo",
    })
