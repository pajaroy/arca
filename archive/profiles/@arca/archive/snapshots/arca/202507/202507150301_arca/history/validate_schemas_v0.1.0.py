"""
---
metadatos:
  id_unico: "scr-py-002"
  tipo: "core"
  nombre: "validate_schemas.py"
  version: "0.1.0"
  estado: "archivado"
  dependencias: ["load_config.py"]
  descripcion: "Valida estructura de schemas (JSON/SQL/YAML)"
---
"""

from pathlib import Path  # ¡Esta línea faltaba!
from load_config import CONFIG
import json

def validar_schemas():
    """Valida los schemas definidos en la configuración"""
    schemas = CONFIG.get('schemas', {})
    
    if not schemas:
        print("⚠️ No hay schemas definidos en config.yaml")
        return False
    
    print("\n🔍 Validando schemas:")
    resultados = {}
    
    for schema_type, schema_path in schemas.items():
        try:
            # Construir ruta absoluta (base_path + ruta relativa)
            ruta_completa = Path(CONFIG['base_path']) / schema_path
            
            # Verificar si el archivo existe
            if not ruta_completa.exists():
                resultados[schema_type] = f"❌ No encontrado en {ruta_completa}"
                continue
            
            # Leer contenido
            with open(ruta_completa, 'r') as f:
                contenido = f.read()
                if not contenido.strip():
                    resultados[schema_type] = f"⚠️ Archivo vacío en {schema_path}"
                else:
                    resultados[schema_type] = f"✅ Válido ({len(contenido)} bytes)"
            
        except Exception as e:
            resultados[schema_type] = f"❌ Error: {str(e)}"
    
    # Mostrar resultados
    for schema_type, mensaje in resultados.items():
        print(f"- {schema_type.upper()}: {mensaje}")
    
    return all("✅" in m for m in resultados.values())

if __name__ == "__main__":
    print(f"\nValidando configuración de {CONFIG.get('project', 'Proyecto')}:")
    print(f"Ruta base: {CONFIG.get('base_path', 'No definida')}")
    
    if validar_schemas():
        print("\n🎉 Todos los schemas son válidos")
    else:
        print("\n⚠️ Algunos schemas tienen problemas")