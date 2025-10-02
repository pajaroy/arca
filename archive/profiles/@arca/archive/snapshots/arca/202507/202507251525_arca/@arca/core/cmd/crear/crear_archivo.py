# utils/file_manager.py

from pathlib import Path
from datetime import datetime
from utils.load_config.load_config import load_config
from utils.load_schema.load_schema import load_schema
from utils.hash_utils.hash_utils import hash_file
from utils.uuid_utils.uuid_utils import generar_uuid
from utils.logger.logger import log_event
from utils.indexar_documento.indexar_documento import indexar_documento

from ruamel.yaml import YAML
from io import StringIO

# Cargar configuración y schema
config = load_config()
schemas = load_schema()
base_path = Path(config["paths"]["base"])
data_dir = base_path / config["paths"]["data"]
schema_yaml = schemas["frontmatter"]  # Debe existir 'frontmatter' en tus schemas

def generar_frontmatter(campos_schema: dict, tipo: str, nombre: str, autor: str) -> dict:
    now = datetime.now().isoformat()
    frontmatter = {}
    for campo in campos_schema:
        if campo == "uuid":
            frontmatter[campo] = generar_uuid()
        elif campo == "tipo":
            frontmatter[campo] = tipo
        elif campo == "formato":
            frontmatter[campo] = tipo
        elif campo == "nombre":
            frontmatter[campo] = nombre
        elif campo == "fecha_creacion" or campo == "fecha_modificacion":
            frontmatter[campo] = now
        elif campo == "autor":
            frontmatter[campo] = autor
        elif campo == "descripcion":
            frontmatter[campo] = "Archivo creado automáticamente"
        elif campo == "version":
            frontmatter[campo] = "0.1.0"
        elif campo == "estado":
            frontmatter[campo] = "activo"
        elif campo == "hash_integridad":
            frontmatter[campo] = ""  # se completa después
        else:
            frontmatter[campo] = ""
    return frontmatter

def crear_archivo(
    nombre: str,
    contenido: str = "",
    tipo: str = "txt",
    autor: str = "desconocido",
    destino: Path = None,
) -> Path:
    config = load_config()
    base_path = Path(config["paths"]["base"])
    if destino is None:
        destino = Path(config["paths"]["data"])
        destino = base_path / destino

    # Seguridad: prohibir fuera del base_path
    if not str(destino.resolve()).startswith(str(base_path.resolve())):
        raise ValueError("Destino fuera del directorio base. Operación no permitida.")

    archivo = destino / f"{nombre}.{tipo}"
    archivo.parent.mkdir(parents=True, exist_ok=True)

    metadata = generar_frontmatter(schema_yaml, tipo, nombre, autor)

    # Armar encabezado
    yaml = YAML()
    s = StringIO()
    yaml.dump(metadata, s)
    frontmatter_str = s.getvalue()

    if tipo == "md":
        frontmatter_formatted = f"---\n{frontmatter_str}---\n"
    elif tipo == "yaml":
        frontmatter_formatted = f"{frontmatter_str}"
    else:
        frontmatter_formatted = ""

    # Escribir encabezado y contenido
    if frontmatter_formatted:
        archivo.write_text(f"{frontmatter_formatted}\n{contenido}")
    else:
        archivo.write_text(contenido)

    metadata["hash_integridad"] = hash_file(archivo)

    indexar_documento(metadata)
    log_event("info", "file_manager", f"Archivo creado: {archivo}", accion="crear")

    return archivo
