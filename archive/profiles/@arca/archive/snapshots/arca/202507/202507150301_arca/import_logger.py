"""
---
metadatos:
  id_unico: "scr-py-006"
  tipo: "utilidad"
  nombre: "import_logger.py"
  version: "0.1.0"
  estado: "activo"
  dependencias: ["logger.py"]
  descripcion: "Ejemplo básico de uso del logger ARCA"
---
"""
from logger import logger

# Ejemplo de uso
logger.log("INFO", "import_logger", "Inicio de prueba")
logger.log("ERROR", "import_logger", "Prueba fallida", {"stacktrace": "None"})

print("✅ Logs enviados. Revisa", logger.ruta)