from core.cmd.crear.crear_archivo import crear_archivo
from pathlib import Path
from utils.load_config.load_config import load_config

config = load_config()
base_path = Path(config["paths"]["base"])

crear_archivo(
    nombre="README4",
    contenido="Este archivo fue generado automáticamente.\n",
    tipo="yaml",
    autor="Bird",
    destino=base_path  # Opcional, default es carpeta de datos
)

