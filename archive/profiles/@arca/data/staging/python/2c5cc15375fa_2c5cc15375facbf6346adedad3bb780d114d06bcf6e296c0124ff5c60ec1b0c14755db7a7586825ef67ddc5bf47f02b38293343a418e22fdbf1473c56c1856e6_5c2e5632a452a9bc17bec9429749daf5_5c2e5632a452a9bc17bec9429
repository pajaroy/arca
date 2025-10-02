#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script CLI para agregar entradas estructuradas a la bitácora viva de ALMA_RESIST
(Versión instrumentada para debugging)
"""

import os
import sys
import argparse
import yaml
import shutil
from datetime import datetime
from pathlib import Path

# Configuración básica
BITACORA_FILE = "/home/bird/alma_resist/control_central/bitacora/bitacora_viva.yaml"
BACKUP_DIR = "/home/bird/alma_resist/control_central/bitacora/backups"
MINIMAL_ENTRY_FIELDS = ['fecha', 'accion', 'descripcion', 'motivo', 'ejecutado_por', 'estado']

def debug_print(label, data):
    """Función auxiliar para prints de debugging"""
    print(f"\n=== DEBUG {label} ===")
    print(f"Tipo: {type(data)}")
    print("Contenido:")
    print(data)
    print("="*(12 + len(label)), "\n")

def validar_estructura_bitacora(data):
    """Valida la estructura básica del archivo de bitácora"""
    debug_print("VALIDACION - INPUT", data)
    if not isinstance(data, dict):
        raise ValueError("La bitácora debe ser un diccionario")
    if 'entradas' not in data:
        raise ValueError("Falta sección 'entradas' en la bitácora")
    if not isinstance(data['entradas'], list):
        raise ValueError("Las entradas deben ser una lista")
    debug_print("VALIDACION - OK", "Estructura válida")

def hacer_backup(archivo):
    """Crea un backup del archivo antes de modificarlo"""
    debug_print("BACKUP - ARCHIVO ORIGINAL", archivo)
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"bitacora_backup_{timestamp}.yaml")
        shutil.copy2(archivo, backup_file)
        debug_print("BACKUP - CREADO", backup_file)
        return backup_file
    except Exception as e:
        debug_print("BACKUP - ERROR", str(e))
        raise

def cargar_bitacora(archivo):
    """Carga y valida el archivo de bitácora"""
    debug_print("CARGA - ARCHIVO", archivo)
    try:
        with open(archivo, 'r') as f:
            data = yaml.safe_load(f) or {'entradas': []}
        debug_print("CARGA - DATOS LEIDOS", data)
        validar_estructura_bitacora(data)
        return data
    except Exception as e:
        debug_print("CARGA - ERROR", str(e))
        sys.exit(1)

def guardar_bitacora(archivo, data):
    """Guarda los datos en el archivo de bitácora con validación"""
    debug_print("GUARDADO - INPUT DATA", data)
    try:
        validar_estructura_bitacora(data)
        debug_print("GUARDADO - ARCHIVO DESTINO", archivo)
        with open(archivo, 'w') as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
            f.flush()  # Forzar escritura a disco
            os.fsync(f.fileno())  # Sincronizar con sistema de archivos
        debug_print("GUARDADO - COMPROBACION", f"Archivo {archivo} modificado: {datetime.fromtimestamp(os.path.getmtime(archivo))}")
    except Exception as e:
        debug_print("GUARDADO - ERROR", str(e))
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
    
    if hasattr(args, 'tags') and args.tags:
        entrada['tags'] = args.tags.split(',')
    
    debug_print("NUEVA ENTRADA CREADA", entrada)
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
    debug_print("ARGUMENTOS RECIBIDOS", vars(args))
    
    # Verificar que el archivo de bitácora exista
    if not os.path.exists(args.bitacora):
        debug_print("ERROR", f"Archivo de bitácora no encontrado: {args.bitacora}")
        sys.exit(1)
    
    debug_print("PERMISOS ARCHIVO", f"Lectura: {os.access(args.bitacora, os.R_OK)} Escritura: {os.access(args.bitacora, os.W_OK)}")
    
    # Crear backup antes de cualquier modificación
    try:
        backup_path = hacer_backup(args.bitacora)
        print(f"Backup creado en: {backup_path}")
    except Exception as e:
        debug_print("BACKUP FALLIDO", str(e))
        sys.exit(1)
    
    # Cargar bitácora existente
    bitacora_data = cargar_bitacora(args.bitacora)
    debug_print("BITACORA CARGADA", bitacora_data)
    
    # Crear y agregar nueva entrada
    nueva_entrada = crear_nueva_entrada(args)
    bitacora_data['entradas'].append(nueva_entrada)
    debug_print("BITACORA MODIFICADA", bitacora_data)
    
    # Guardar cambios
    guardar_bitacora(args.bitacora, bitacora_data)
    print("Entrada agregada exitosamente a la bitácora")
    
    # Verificación final
    with open(args.bitacora, 'r') as f:
        contenido_final = yaml.safe_load(f)
        debug_print("CONTENIDO FINAL", contenido_final)

if __name__ == "__main__":
    main()