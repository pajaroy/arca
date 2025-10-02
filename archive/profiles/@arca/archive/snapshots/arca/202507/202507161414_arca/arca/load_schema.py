"""METADATOS\nuuid: 4b7db324-f45a-4e22-9522-61a8dc7b1b03
tipo: py
nombre: load_schema
version: 0.1.0
estado: activo
fecha_creacion: '2025-07-16T01:59:38.192416'
fecha_modificacion: '2025-07-16T01:59:38.192467'
autor: Bird
descripcion: Carga schemas
hash_integridad: c17a58547b1f409cb51a12336aae735122e72282a231a910b4093a30f5f48044
\n"""

from pathlib import Path
import yaml
from load_config import load_config

def load_schema():
    """
    Carga el schema YAML desde la ruta definida en config.yaml.
    Devuelve un diccionario con el schema completo.
    """
    CONFIG = load_config()
    schema_path = Path(CONFIG['config']['schema_path'])
    if not schema_path.exists():
        raise FileNotFoundError(f"No se encontró el schema en: {schema_path}")
    with open(schema_path, "r") as f:
        return yaml.safe_load(f)

# Ejemplo de uso rápido
if __name__ == "__main__":
    schema = load_schema()
    print(schema)
