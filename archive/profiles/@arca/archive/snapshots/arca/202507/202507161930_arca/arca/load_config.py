"""METADATOS\nuuid: 275e1086-2c82-4be3-8300-230312a10946
tipo: py
nombre: load_config
version: 0.1.0
estado: activo
fecha_creacion: '2025-07-16T01:53:13.277024'
fecha_modificacion: '2025-07-16T01:53:13.277072'
autor: Bird
descripcion: Cargar configuracion desde config/config.yaml
hash_integridad: 512afd8d2333a83d832c2d8e682a7bceb5f9601e3fb08793f664b1b4b93dd71c
\n"""

from pathlib import Path
import yaml

def load_config():
    base = Path(__file__).parent  # directorio del script load_config.py
    config_path = base / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

