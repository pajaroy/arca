"""
---
metadatos:
  id_unico: "scr-py-002b"
  tipo: "core"
  nombre: "validate_schemas.py"
  version: "0.2.0"
  dependencias: 
    - "load_config.py"
    - "logger.py"  # Nueva dependencia
  descripcion: "Valida schemas y registra resultados en logs"
---
"""
from pathlib import Path
from load_config import CONFIG
from logger import logger  # Nuevo import
import json

def validar_schemas():
    """Valida schemas y muestra resultados por consola + logs"""
    # Configuración inicial
    schemas = CONFIG.get('schemas', {})
    resultados = {}
    
    # Logger + Consola
    def _log_consola(nivel: str, mensaje: str):
        logger.log(nivel, "validate_schemas", mensaje)
        print(f"[{nivel}] {mensaje}")  # Nuevo: muestra en consola también

    _log_consola("INFO", "Iniciando validación de schemas")
    
    if not schemas:
        _log_consola("WARNING", "No hay schemas definidos en config.yaml")
        return False

    for schema_type, schema_path in schemas.items():
        try:
            ruta = Path(CONFIG['base_path']) / schema_path
            if not ruta.exists():
                msg = f"{schema_type.upper()}: ❌ No encontrado en {ruta}"
                resultados[schema_type] = False
                _log_consola("ERROR", msg)
                continue
                
            with open(ruta, 'r') as f:
                contenido = f.read()
                valido = bool(contenido.strip())
                resultados[schema_type] = valido
                
                msg = f"{schema_type.upper()}: {'✅' if valido else '⚠️'} ({len(contenido)} bytes)"
                _log_consola("INFO", msg)

        except Exception as e:
            _log_consola("ERROR", f"{schema_type.upper()}: ❌ Error - {str(e)}")
            resultados[schema_type] = False

    # Resumen final
    if all(resultados.values()):
        _log_consola("INFO", "🎉 Todos los schemas son válidos")
    else:
        _log_consola("WARNING", f"⚠️ Problemas en: {[k for k,v in resultados.items() if not v]}")

    return all(resultados.values())