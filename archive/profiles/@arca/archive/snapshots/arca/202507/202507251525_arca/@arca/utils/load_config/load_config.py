# utils/load_config.py

from pathlib import Path
import sys

try:
    from ruamel.yaml import YAML
except ImportError:
    sys.exit("[ERROR] Falta la librería 'ruamel.yaml'. Instalála primero.")

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"

def load_config(path: Path = CONFIG_PATH) -> dict:
    """
    Carga la configuración del sistema desde un archivo YAML.
    Parámetros:
        path (Path): Ruta al archivo YAML de configuración.
    Retorna:
        dict: Diccionario con los valores de configuración.
    """
    if not path.is_file():
        sys.exit(f"[ALMA-CONFIG][CRÍTICO] Archivo no encontrado: {path}")

    yaml = YAML(typ="safe")
    try:
        with path.open("r", encoding="utf-8") as f:
            config = yaml.load(f)
            return config
    except Exception as e:
        sys.exit(f"[ALMA-CONFIG][CRÍTICO] Error al leer configuración: {e}")
