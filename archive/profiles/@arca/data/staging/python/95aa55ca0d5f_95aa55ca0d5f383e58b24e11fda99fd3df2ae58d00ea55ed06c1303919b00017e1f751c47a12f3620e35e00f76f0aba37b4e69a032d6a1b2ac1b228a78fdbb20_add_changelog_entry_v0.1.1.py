#!/usr/bin/env python3
"""
Script CLI mejorado para changelog de ALMA_RESIST con rutas configurables y manejo robusto de listas
"""

import argparse
import os
import shutil
import datetime
import sys
import yaml

# Valor por defecto para el archivo changelog
DEFAULT_CHANGELOG = "changelog.yaml"

def parse_lista(valor, separador=','):
    """Convierte strings en listas usando separador, mantiene listas existentes"""
    if valor is None:
        return []
    if isinstance(valor, list):
        return valor
    return [item.strip() for item in valor.split(separador) if item.strip()]

def asegurar_directorio(ruta_archivo):
    """Crea directorios necesarios para la ruta si no existen"""
    directorio = os.path.dirname(ruta_archivo)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)
        print(f"Directorio creado: {directorio}")

def validar_estructura(data):
    """Valida la estructura básica del changelog"""
    if not isinstance(data, dict):
        raise ValueError("El archivo no es un diccionario válido")
    if 'changelog' not in data:
        raise KeyError("Falta la clave principal 'changelog'")
    if not isinstance(data['changelog'], list):
        raise TypeError("'changelog' debe ser una lista")
    return True

def crear_changelog(ruta_archivo):
    """Crea un archivo changelog inicial si no existe"""
    base = {'changelog': []}
    asegurar_directorio(ruta_archivo)
    with open(ruta_archivo, 'w') as f:
        yaml.safe_dump(base, f, allow_unicode=True, sort_keys=False)
    return base

def cargar_changelog(ruta_archivo):
    """Carga y valida el archivo changelog existente"""
    try:
        # Si el archivo existe pero está vacío
        if os.path.exists(ruta_archivo) and os.path.getsize(ruta_archivo) == 0:
            return crear_changelog(ruta_archivo)
            
        with open(ruta_archivo, 'r') as f:
            data = yaml.safe_load(f) or {}
        
        validar_estructura(data)
        return data
    
    except FileNotFoundError:
        return crear_changelog(ruta_archivo)
    
    except Exception as e:
        raise RuntimeError(f"Error en la estructura del archivo: {str(e)}")

def hacer_backup(ruta_archivo):
    """Crea un backup con timestamp del archivo actual"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{ruta_archivo}.backup_{timestamp}"
    shutil.copy2(ruta_archivo, backup_file)
    return backup_file

def version_existe(changelog_data, version):
    """Verifica si una versión ya existe en el changelog"""
    return any(entry.get('version') == version for entry in changelog_data['changelog'])

def crear_entrada(args):
    """Construye el diccionario de la nueva entrada"""
    entry = {
        'version': args.version,
        'fecha': args.fecha,
        'autor': args.autor,
        'cambios': parse_lista(args.cambios, separador='|'),
        'impacto': args.impacto
    }
    
    if args.tags:
        entry['tags'] = parse_lista(args.tags)
    
    return entry

def mostrar_resumen(entry, ruta_archivo):
    """Muestra un resumen de la entrada agregada"""
    print("\n" + "="*50)
    print("ENTRADA AGREGADA AL CHANGELOG:")
    print("="*50)
    print(f"- Archivo:   {ruta_archivo}")
    print(f"- Versión:   {entry['version']}")
    print(f"- Fecha:     {entry['fecha']}")
    print(f"- Autor:     {entry['autor']}")
    print("- Cambios:")
    for i, cambio in enumerate(entry['cambios'], 1):
        print(f"  {i}. {cambio}")
    print(f"- Impacto:   {entry['impacto']}")
    if entry.get('tags'):
        print(f"- Tags:      {', '.join(entry['tags'])}")
    print("="*50 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description='Agregar entradas al changelog de ALMA_RESIST',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Campos requeridos
    parser.add_argument('--version', required=True, help='Versión semántica (ej: "0.1.2")')
    parser.add_argument('--cambios', required=True, 
                        help='Lista de cambios (separados por pipes |)')
    parser.add_argument('--impacto', required=True, 
                        help='Resumen del impacto general de esta versión')
    parser.add_argument('--autor', required=True, 
                        help='Nombre del autor o autores')
    
    # Campos opcionales
    parser.add_argument('--fecha', default=datetime.date.today().isoformat(),
                        help='Fecha en formato ISO 8601 (YYYY-MM-DD)')
    parser.add_argument('--tags', 
                        help='Etiquetas para clasificación (separadas por comas)')
    
    # Nuevo argumento para ruta configurable
    parser.add_argument('--changelog', default=DEFAULT_CHANGELOG,
                        help='Ruta personalizada del archivo changelog')
    
    args = parser.parse_args()
    
    try:
        # Validación básica de versión
        if not args.version.replace('.', '').isdigit():
            print("Advertencia: La versión podría no ser semántica válida", file=sys.stderr)
        
        # Cargar o crear changelog
        changelog_data = cargar_changelog(args.changelog)
        
        # Validar unicidad de versión
        if version_existe(changelog_data, args.version):
            raise ValueError(f"La versión {args.version} ya existe en el changelog")
        
        # Crear backup antes de modificar
        if os.path.exists(args.changelog):
            backup_path = hacer_backup(args.changelog)
            print(f"Backup creado: {backup_path}")
        
        # Crear nueva entrada
        nueva_entrada = crear_entrada(args)
        
        # Insertar al principio de la lista
        changelog_data['changelog'].insert(0, nueva_entrada)
        
        # Validar estructura final
        validar_estructura(changelog_data)
        
        # Guardar archivo actualizado
        asegurar_directorio(args.changelog)
        with open(args.changelog, 'w') as f:
            yaml.safe_dump(changelog_data, f, allow_unicode=True, sort_keys=False)
        
        # Mostrar resumen
        mostrar_resumen(nueva_entrada, args.changelog)
        
    except Exception as e:
        print(f"\nERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()