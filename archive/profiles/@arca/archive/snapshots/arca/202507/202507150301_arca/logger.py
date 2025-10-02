"""
---
metadatos:
  id_unico: "scr-py-005c"
  tipo: "core"
  nombre: "logger.py"
  version: "0.1.2"
  estado: "activo"
  dependencias: ["load_config.py"]
  descripcion: "Logger que escribe directamente en archivo especificado en config"
---
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from load_config import CONFIG

class LoggerARCA:
    def __init__(self):
        self._buffer = []
        self.archivo_log = Path(CONFIG["base_path"]) / CONFIG["logging"]["ruta"]
        
    def log(self, nivel: str, modulo: str, mensaje: str):
        log_entry = {
            "timestamp": datetime.now().isoformat(),  # Usamos string ISO
            "nivel": nivel,
            "modulo": modulo,
            "mensaje": mensaje
        }
        try:
            # Si el archivo existe y no está vacío
            if self.archivo_log.exists() and self.archivo_log.stat().st_size > 0:
                df_existente = pd.read_parquet(self.archivo_log)
                df_nuevo = pd.DataFrame([log_entry])
                pd.concat([df_existente, df_nuevo]).to_parquet(self.archivo_log)
            else:
                # Primera escritura
                pd.DataFrame([log_entry]).to_parquet(self.archivo_log)
                
        except Exception as e:
            print(f"❌ Error en logger (archivo: {self.archivo_log}): {str(e)}")

logger = LoggerARCA()