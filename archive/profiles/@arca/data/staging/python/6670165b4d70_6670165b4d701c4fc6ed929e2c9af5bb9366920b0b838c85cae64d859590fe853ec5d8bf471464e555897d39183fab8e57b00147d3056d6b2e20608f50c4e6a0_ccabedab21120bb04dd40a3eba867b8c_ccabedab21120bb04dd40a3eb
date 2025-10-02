#!/usr/bin/env python3
"""
Script CLI para agregar entradas estructuradas al changelog.yaml de ALMA_RESIST
"""

import argparse
import os
import shutil
import datetime
import sys
import yaml

# Nombre del archivo de changelog
CHANGELOG_FILE = "changelog.yaml"

def validar_estructura(data):
    """Valida la estructura básica del changelog"""
    if not isinstance(data, dict):
        raise ValueError("El archivo no es un diccionario válido")
    if 'changelog' not in data:
        raise KeyError("Falta la clave principal 'changelog'")
    if not isinstance(data['changelog'], list):
        raise TypeError("'changelog' debe ser una lista")
    return True

def crear_changelog():
    """Crea un archivo changelog inicial si no existe"""
    base = {'changelog': []}
    with open(CHANGELOG_FILE, 'w') as f:
        yaml.safe_dump(base, f, allow_unicode=True, sort_keys=False)
    return base

def cargar_changelog():
    """Carga y valida el archivo changelog existente"""
    try:
        with open(CHANGELOG_FILE, 'r') as f:
            data = yaml.safe_load(f) or {}
        
        validar_estructura(data)
        return data
    
    except FileNotFoundError:
        return crear_changelog()
    
    except Exception as e:
        raise RuntimeError(f"Error en la estructura del archivo: {str(e)}")

def hacer_backup():
    """Crea un backup con timestamp del archivo actual"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{CHANGELOG_FILE}.backup_{timestamp}"
    shutil.copy2(CHANGELOG_FILE, backup_file)
    return backup_file

def version_existe(changelog_data, version):
    """Verifica si una versión ya existe en el changelog"""
    return any(entry['version'] == version for entry in changelog_data['changelog'])

def crear_entrada(args):
    """Construye el diccionario de la nueva entrada"""
    entry = {
        'version': args.version,
        'fecha': args.fecha,
        'autor': args.autor,
        'cambios': args.cambios.split('|') if isinstance(args.cambios, str) else args.cambios,
        'impacto': args.impacto
    }
    
    if args.tags:
        entry['tags'] = args.tags.split(',') if isinstance(args.tags, str) else args.tags
    
    return entry

def mostrar_resumen(entry):
    """Muestra un resumen de la entrada agregada"""
    print("\nEntrada agregada al changelog:")
    print(f"- Versión: {entry['version']}")
    print(f"- Fecha: {entry['fecha']}")
    print(f"- Autor: {entry['autor']}")
    print("- Cambios:")
    for cambio in entry['cambios']:
        print(f"  • {cambio}")
    print(f"- Impacto: {entry['impacto']}")
    if 'tags' in entry:
        print(f"- Tags: {', '.join(entry['tags'])}")

def main():
    parser = argparse.ArgumentParser(
        description='Agregar entradas al changelog de ALMA_RESIST',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Campos requeridos
    parser.add_argument('--version', required=True, help='Versión semántica (ej: "0.1.2")')
    parser.add_argument('--cambios', required=True, 
                        help='Lista de cambios (separados por pipes | si se usa CLI)')
    parser.add_argument('--impacto', required=True, 
                        help='Resumen del impacto general de esta versión')
    parser.add_argument('--autor', required=True, 
                        help='Nombre del autor o autores')
    
    # Campos opcionales
    parser.add_argument('--fecha', default=datetime.date.today().isoformat(),
                        help='Fecha en formato ISO 8601 (YYYY-MM-DD)')
    parser.add_argument('--tags', 
                        help='Etiquetas para clasificación (separadas por comas)')
    
    args = parser.parse_args()
    
    try:
        # Cargar o crear changelog
        changelog_data = cargar_changelog()
        
        # Validar unicidad de versión
        if version_existe(changelog_data, args.version):
            raise ValueError(f"La versión {args.version} ya existe en el changelog")
        
        # Crear backup antes de modificar
        if os.path.exists(CHANGELOG_FILE):
            backup_path = hacer_backup()
            print(f"Backup creado: {backup_path}")
        
        # Crear nueva entrada
        nueva_entrada = crear_entrada(args)
        
        # Insertar al principio de la lista
        changelog_data['changelog'].insert(0, nueva_entrada)
        
        # Validar estructura final
        validar_estructura(changelog_data)
        
        # Guardar archivo actualizado
        with open(CHANGELOG_FILE, 'w') as f:
            yaml.safe_dump(changelog_data, f, allow_unicode=True, sort_keys=False)
        
        # Mostrar resumen
        mostrar_resumen(nueva_entrada)
        print(f"\nChangelog actualizado en {CHANGELOG_FILE}")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()