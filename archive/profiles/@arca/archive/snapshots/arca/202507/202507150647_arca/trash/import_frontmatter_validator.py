"""
---
metadatos:
  id_unico: "scr-py-008"
  tipo: "utilidad"
  nombre: "import_frontmatter_validator.py"
  version: "0.1.0"
  estado: "archivado"
  dependencias: ["frontmatter_validator.py"]
  descripcion: "Ejemplo de importación básica de frontmatter_validator"
---
"""
from frontmatter_validator import FrontmatterValidator

validator = FrontmatterValidator()

# Procesar archivos específicos
validator.procesar_ruta(["archivo1.md", "archivo2.py"])

# Procesar directorio recursivamente
validator.procesar_ruta(["directorio/"], recursivo=True)