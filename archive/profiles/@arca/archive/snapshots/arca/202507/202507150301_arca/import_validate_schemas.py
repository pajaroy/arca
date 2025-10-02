"""
---
metadatos:
  id_unico: "scr-py-004"
  tipo: "utilidad"
  nombre: "import_validate_schemas.py"
  version: "0.1.0"
  estado: "activo"
  dependencias: ["validate_schemas.py"]
  descripcion: "Ejemplo de uso de validate_schemas"
---
"""
from validate_schemas import validar_schemas

if validar_schemas():
    print("✅ Schemas válidos")
else:
    print("❌ Hay errores en los schemas")