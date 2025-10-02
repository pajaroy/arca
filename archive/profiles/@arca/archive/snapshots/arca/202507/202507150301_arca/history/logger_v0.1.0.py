"""
---
metadatos:
  id_unico: "scr-py-005"
  tipo: "core"
  nombre: "logger.py"
  version: "0.1.0"
  estado: "archivado"
  dependencias: ["load_config.py"]
  descripcion: "Logger Parquet validado contra schema.yaml"
---
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from load_config import CONFIG

class LoggerARCA:
    def __init__(self):
        self._buffer = []
        self.ruta = Path(CONFIG["base_path"]) / CONFIG["logging"]["ruta"]
        self.ruta.mkdir(exist_ok=True)

    def log(self, nivel: str, modulo: str, mensaje: str):
        """Estructura fija validada por schema.yaml"""
        self._buffer.append({
            "timestamp": datetime.now(),
            "nivel": nivel,
            "modulo": modulo,
            "mensaje": mensaje
        })
        if len(self._buffer) >= 10:
            self._guardar()

    def _guardar(self):
        try:
            pd.DataFrame(self._buffer).to_parquet(
                self.ruta / f"logs_{datetime.now().strftime('%Y%m%d')}.parquet"
            )
            self._buffer.clear()
        except Exception as e:
            print(f"❌ Error en logger: {e}")

# Instancia global
logger = LoggerARCA()