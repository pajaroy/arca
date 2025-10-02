"""
---
metadatos:
  id_unico: "scr-py-003"
  tipo: "utilidad"
  nombre: "import_load_config.py"
  version: "0.1.0"
  estado: "activo"
  dependencias: ["load_config.py"]
  descripcion: "Ejemplo de importación básica de load_config"
---
"""

from load_config import CONFIG

print("Autor:", CONFIG.get("default_author", "Desconocido"))