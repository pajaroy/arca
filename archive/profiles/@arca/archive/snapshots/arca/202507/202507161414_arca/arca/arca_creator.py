"""METADATOS\nuuid: bc092cba-c66f-4506-88cf-c1e83089b4c3
tipo: py
nombre: arca_creator
version: 0.1.0
estado: activo
fecha_creacion: '2025-07-16T01:36:10.804255'
fecha_modificacion: '2025-07-16T01:36:10.804310'
autor: Bird
descripcion: Script para cargar config validar schemas y crear archivo hasheado
hash_integridad: 9267658a23e8de68521f15dba180d307afba6031980a63d5d10c6a32ad31b3e3
\n"""

from load_config import load_config
from load_schema import load_schema
from hash_utils import calc_hash_string
from indexar_entrada import indexar_archivo
import yaml
import uuid
from datetime import datetime
from pathlib import Path

CONFIG = load_config()
SCHEMA = load_schema()

def generar_frontmatter(campos_schema, formato_archivo, args={}):
    frontmatter = {}
    for campo, default in campos_schema.items():
        if campo == "uuid":
            frontmatter[campo] = str(uuid.uuid4())
        elif campo in ["fecha_creacion", "fecha_modificacion"]:
            frontmatter[campo] = datetime.now().isoformat()
        elif campo == "formato":
            frontmatter[campo] = formato_archivo   # REGISTRA el formato usado
        elif campo == "hash_integridad":
            frontmatter[campo] = ""
        elif campo in args:
            frontmatter[campo] = args[campo]
        else:
            frontmatter[campo] = default
    return frontmatter

def validate_frontmatter(frontmatter, schema):
    for field in schema['metadatos_frontmatter'].keys():
        if field not in frontmatter:
            raise ValueError(f"Campo requerido faltante: {field}")
    return True

def crear_archivo(formato_archivo, tipo, nombre, subdirectorio="", **kwargs):
    """
    Crea un archivo con metadatos en la ruta indicada. Si el directorio no existe, lo crea.
    - formato_archivo: 'yaml', 'json', etc.
    - tipo: tipo lógico ('docs', 'modelo', etc)
    - nombre: nombre del archivo (sin extensión)
    - subdirectorio: ruta relativa dentro de base_path (opcional)
    - kwargs: autor, descripcion, etc.
    """
    formatos = CONFIG['config']['formatos_soportados']
    fmt = formatos.get(formato_archivo)
    if not fmt:
        raise ValueError(f"Formato de archivo no soportado: {formato_archivo}")

    delimiter = fmt['delimiter']
    end_delimiter = fmt.get('end_delimiter', delimiter)
    frontmatter_type = fmt['frontmatter_type']

    campos_schema = SCHEMA['metadatos_frontmatter']
    args = {"tipo": tipo, "nombre": nombre}
    args.update(kwargs)

    frontmatter = generar_frontmatter(campos_schema, formato_archivo, args)
    validate_frontmatter(frontmatter, SCHEMA)

    # Serializar y calcular hash (a string)
    if frontmatter_type == "yaml":
        frontmatter_str = delimiter + yaml.dump(frontmatter, sort_keys=False) + end_delimiter
    elif frontmatter_type == "json":
        import json
        frontmatter_str = json.dumps(frontmatter, indent=2)
    else:
        raise NotImplementedError(f"Tipo de frontmatter no soportado: {frontmatter_type}")

    # Calcular hash_integridad
    hash_val = calc_hash_string(frontmatter_str)
    frontmatter["hash_integridad"] = hash_val

    # Re-serializar con hash ya puesto
    if frontmatter_type == "yaml":
        frontmatter_str = delimiter + yaml.dump(frontmatter, sort_keys=False) + end_delimiter
    elif frontmatter_type == "json":
        import json
        frontmatter_str = json.dumps(frontmatter, indent=2)

    # ----------- CREAR DIRECTORIO Y ARCHIVO -----------
    base_path = Path(CONFIG['config']['base_path'])
    target_dir = base_path / subdirectorio if subdirectorio else base_path
    target_dir.mkdir(parents=True, exist_ok=True)
    ruta = target_dir / f"{nombre}.{formato_archivo}"
    if ruta.exists():
        raise FileExistsError(f"El archivo ya existe: {ruta}")
    with open(ruta, 'w') as f:
        f.write(frontmatter_str)

    print(f"Archivo creado: {ruta}")

    # ----------- INDEXAR ARCHIVO -----------
    index_estructura = CONFIG['config']['index_estructura']
    index_info = dict(index_estructura)  # copia
    index_info.update({
        "uuid": frontmatter.get("uuid"),
        "nombre": nombre,
        "ruta": str(ruta.relative_to(base_path)),  # Siempre ruta relativa al proyecto
        "tipo": tipo,
        "formato": formato_archivo,
        "hash_integridad": hash_val,
        "fecha_creacion": frontmatter.get("fecha_creacion"),
        "fecha_modificacion": frontmatter.get("fecha_modificacion"),
        "autor": frontmatter.get("autor"),
        "descripcion": frontmatter.get("descripcion"),
    })
    indexar_archivo(index_info)

if __name__ == "__main__":
    # Ejemplo de uso
    crear_archivo(
        "yaml",           # formato_archivo
        "docs",           # tipo lógico
        "test_modulo",    # nombre
        subdirectorio="documentacion",   # crea /documentacion si no existe
        autor="Bird",
        descripcion="Archivo de ejemplo"
    )
