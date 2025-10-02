"""
---
metadatos:
  id_unico: "scr-py-005b"
  tipo: "core"
  nombre: "logger.py"
  version: "0.1.1"
  estado: "archivado"
  dependencias: ["load_config.py"]
  descripcion: "Logger que usa ruta exacta de config.yaml"
---
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from load_config import CONFIG

class LoggerARCA:
    def __init__(self):
        self._buffer = []
        cfg = CONFIG.get("logging", {})
        
        # Ruta ABSOLUTA desde config (base_path + logging.ruta)
        self.ruta_logs = Path(CONFIG["base_path"]) / cfg.get("ruta", "logs")
        self.ruta_logs.mkdir(exist_ok=True)
        
        # Nombre de archivo personalizable
        self.nombre_base = cfg.get("nombre_archivo", "arca_logs")

    def log(self, nivel: str, modulo: str, mensaje: str):
        log_entry = {
            "timestamp": datetime.now(),
            "nivel": nivel,
            "modulo": modulo,
            "mensaje": mensaje
        }
        self._buffer.append(log_entry)
        
        if len(self._buffer) >= 5:  # Reduced batch size for testing
            self._guardar()

    def _guardar(self):
        try:
            # Nombre del archivo: [nombre_base]_[fecha].parquet
            fecha = datetime.now().strftime("%Y%m%d")
            archivo = self.ruta_logs / f"{self.nombre_base}_{fecha}.parquet"
            
            pd.DataFrame(self._buffer).to_parquet(archivo)
            self._buffer.clear()
        except Exception as e:
            print(f"❌ Error guardando log: {e}")

# Instancia global
logger = LoggerARCA()