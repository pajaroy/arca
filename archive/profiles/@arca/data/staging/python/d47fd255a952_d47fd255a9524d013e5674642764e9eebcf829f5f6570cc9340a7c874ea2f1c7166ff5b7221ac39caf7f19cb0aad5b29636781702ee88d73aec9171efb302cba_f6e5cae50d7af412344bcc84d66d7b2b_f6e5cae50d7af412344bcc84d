#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script CLI para agregar entradas estructuradas a la bitácora viva de ALMA_RESIST

MVP según especificación IDEA_BASE_BITACORA_SCRIPT_2025-06-06_01
"""

import os
import sys
import argparse
import yaml
import shutil
from datetime import datetime
from pathlib import Path

print("DEBUG: El script arrancó")


# Configuración básica
BITACORA_FILE = "/home/bird/alma_resist/control_central/bitacora/bitacora_viva.yaml"
BACKUP_DIR = "/home/bird/alma_resist/control_central/bitacora/backups"
MINIMAL_ENTRY_FIELDS = ['fecha', 'accion', 'descripcion', 'motivo', 'ejecutado_por', 'estado']

def validar_estructura_bitacora(data):
    """Valida la estructura básica del archivo de bitácora"""
    if not isinstance(data, dict):
        raise ValueError("La bitácora debe ser un diccionario")
    if 'entradas' not in data:
        raise ValueError("Falta sección 'entradas' en la bitácora")
    if not isinstance(data['entradas'], list):
        raise ValueError("Las entradas deben ser una lista")

def hacer_backup(archivo):
    """Crea un backup del archivo antes de modificarlo"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"bitacora_backup_{timestamp}.yaml")
    shutil.copy2(archivo, backup_file)
    return backup_file

def cargar_bitacora(archivo):
    """Carga y valida el archivo de bitácora"""
    try:
        with open(archivo, 'r') as f:
            data = yaml.safe_load(f) or {'entradas': []}
        validar_estructura_bitacora(data)
        return data
    except Exception as e:
        print(f"Error al cargar bitácora: {str(e)}", file=sys.stderr)
        sys.exit(1)

def guardar_bitacora(archivo, data):
    """Guarda los datos en el archivo de bitácora con validación"""
    try:
        validar_estructura_bitacora(data)
        with open(archivo, 'w') as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
    except Exception as e:
        print(f"Error al guardar bitácora: {str(e)}", file=sys.stderr)
        sys.exit(1)

def crear_nueva_entrada(args):
    """Crea un diccionario con los datos de la nueva entrada"""
    entrada = {
        'fecha': args.fecha or datetime.now().isoformat(),
        'accion': args.accion,
        'descripcion': args.descripcion,
        'motivo': args.motivo,
        'ejecutado_por': args.ejecutado_por,
        'estado': args.estado or 'registrado'
    }
    
    # Campos adicionales si existen
    if hasattr(args, 'tags') and args.tags:
        entrada['tags'] = args.tags.split(',')
    
    return entrada

def main():
    # Configuración del parser de argumentos
    parser = argparse.ArgumentParser(
        description="Agrega una entrada a la bitácora viva de ALMA_RESIST",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Argumentos requeridos
    parser.add_argument('--accion', required=True, help="Acción realizada o evento registrado")
    parser.add_argument('--descripcion', required=True, help="Descripción detallada de la acción/evento")
    parser.add_argument('--motivo', required=True, help="Motivo o justificación de la acción")
    parser.add_argument('--ejecutado_por', required=True, help="Persona o sistema que ejecutó la acción")
    
    # Argumentos opcionales
    parser.add_argument('--fecha', help="Fecha en formato ISO (por defecto: ahora)")
    parser.add_argument('--estado', help="Estado inicial de la entrada", default="registrado")
    parser.add_argument('--tags', help="Tags separados por comas para categorización")
    parser.add_argument('--bitacora', help="Ruta alternativa al archivo de bitácora", default=BITACORA_FILE)
    
    args = parser.parse_args()
    
    # Verificar que el archivo de bitácora exista
    if not os.path.exists(args.bitacora):
        print(f"Archivo de bitácora no encontrado: {args.bitacora}", file=sys.stderr)
        sys.exit(1)
    
    # Crear backup antes de cualquier modificación
    backup_path = hacer_backup(args.bitacora)
    print(f"Backup creado en: {backup_path}")
    
    # Cargar bitácora existente
    bitacora_data = cargar_bitacora(args.bitacora)
    
    # Crear y agregar nueva entrada
    nueva_entrada = crear_nueva_entrada(args)
    bitacora_data['entradas'].append(nueva_entrada)
    
    # Guardar cambios
    guardar_bitacora(args.bitacora, bitacora_data)
    print("Entrada agregada exitosamente a la bitácora")

if __name__ == "__main__":
    main()