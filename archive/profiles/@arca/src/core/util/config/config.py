#!/usr/bin/env python3
# ~/@arca/core/util/config/config.py
# Version: 1.0
# Fecha: 2025-08-01
# Autor: Bird
# Reglas de oro:
#  - Siempre mantener explicaciones dentro del script con comentarios
# Descripcion: Script generico de arca para cargar config.yaml 
# Funciones:
#  - Cargar config yaml siempre dos directorios para atras y tomar desde config/config.yaml ././config/config.yaml (asi seria no ?)
#  - El unico root hardcodeado debe ser el del modulo. Ejemplo para el primero y replicable root=~/@arca
# 
# 

from pathlib import Path
import yaml

def load_config():
    """Carga config.yaml desde ../../config/ (relativo al script actual)"""
    config_path = Path(__file__).parent.parent.parent / "config/config.yaml"
    
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"⚠️ Archivo de configuración no encontrado en: {config_path}")
    except yaml.YAMLError:
        raise ValueError("⚠️ Error al parsear config.yaml - Revisa la sintaxis")

# Ejemplo de uso mínimo
if __name__ == "__main__":
    config = load_config()
    print("✓ Configuración cargada correctamente")


# Me qede en la parte de cambiar la configuracion , la ultima duda era si el path base lo marca la parte de 'config_path = Path(__file__).parent.parent.parent / "config/config.yaml"' relativa al script
# De ser asi entonces se tomaria siempre la ruta desde donde esta el archivo , eso indica ? 
# chat: https://chat.deepseek.com/a/chat/s/af811e77-8965-437b-a311-193b890305b4