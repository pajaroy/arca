"""
---
metadatos:
  id_unico: "scr-py-001"
  tipo: "core"
  nombre: "load_config.py"
  version: "0.1.0"
  estado: "activo"
  dependencias: []
  descripcion: "Carga config.yaml y expone CONFIG global"
---
"""

from pathlib import Path
import yaml

# Ruta base (único hardcodeo)
ROOT_PATH = Path("/home/arca/arca")

def cargar_config():
    """Carga config.yaml y verifica estructura básica"""
    try:
        with open(ROOT_PATH / "config.yaml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
            
            # Verificación mínima
            if not config:
                print("⚠️ Configuración vacía o formato incorrecto")
                return {}
            
            print(f"✅ Config cargada | Proyecto: {config.get('project', 'Sin nombre')} | Versión: {config.get('version', 'No especificada')}")
            return config
            
    except Exception as e:
        print(f"❌ Error cargando config: {str(e)}")
        return {}

# Carga automática al importar
CONFIG = cargar_config()