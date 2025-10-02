# ---
# version: "0.2.0"
# tipo: "script"
# schema: "almaresist.bitacora_cli_v1"
# descripcion: "Script CLI auditado para la carga y gestión de bitácoras institucionales ALMA_RESIST. Triple formato, backup automático, validación de metadatos y compatibilidad con protocolos KAEL."
# tags: [bitacora, cli, v0.2.0, institucional, kael, python]
# linked_to: ["../../docs/prompt_add_bitacora/prompt_add_bitacora_entry_v0.2.0.yaml", "../../docs/readme_tecnico/readme_tecnico.yaml", "README.yaml"]
# responsable: "Equipo de Operaciones ALMA_RESIST"
# hash_verificacion: "sha256:pending"
# historial:
#   - "2025-06-17: Release inicial y puesta en producción bajo protocolo KAEL."
# last_modified: "2025-06-17T11:45:00Z"
# last_modified_by: "Kael"
# ---

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALMA_RESIST - Bitácora Institucional v0.2.0
Script CLI para gestión segura de bitácoras con triple formato (YAML/JSON/MD)
"""
import os
import sys
import json
import uuid
import argparse
from datetime import datetime, timezone
from pathlib import Path
import yaml
import hashlib
import logging

# Configuración global
DEFAULT_BITACORA_PATH = "docs/journal/bitacora_viva.yaml"
BACKUP_DIR = "docs/journal/backups"
LOG_DIR = "logs"
VALID_ESTADOS = ["registrado", "en_progreso", "completado", "cancelado", "revisión"]
METADATA_FIELDS = [
    "version", "tipo", "schema", "descripcion", "estructura", "tags", 
    "linked_to", "responsable", "hash_verificacion", "historial", 
    "last_modified", "last_modified_by"
]

# Configuración de logging
def setup_logging(log_dir=None, verbose=False):
    """Configura el sistema de logging"""
    logger = logging.getLogger('bitacora_manager')
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Formato de consola
    console_handler = logging.StreamHandler()
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # Log a archivo si se especifica directorio
    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        log_file = Path(log_dir) / f"bitacora_{datetime.now(timezone.utc).strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

# Funciones de validación
def validate_entry(entry):
    """Valida la estructura de una entrada de bitácora"""
    required_fields = ["fecha", "accion", "descripcion", "motivo", "ejecutado_por"]
    missing = [field for field in required_fields if field not in entry]
    if missing:
        raise ValueError(f"Campos obligatorios faltantes: {', '.join(missing)}")
    
    if "estado" in entry and entry["estado"] not in VALID_ESTADOS:
        raise ValueError(f"Estado inválido: {entry['estado']}. Válidos: {', '.join(VALID_ESTADOS)}")
    
    if "tags" in entry and not isinstance(entry["tags"], list):
        raise ValueError("Tags debe ser una lista de strings")

def validate_metadata(metadata):
    """Valida la estructura del encabezado de metadatos"""
    missing = [field for field in METADATA_FIELDS if field not in metadata]
    if missing:
        raise ValueError(f"Metadatos obligatorios faltantes: {', '.join(missing)}")

# Funciones de manipulación de archivos
def load_bitacora(file_path):
    """Carga una bitácora existente o crea una nueva estructura"""
    path = Path(file_path).absolute()
    
    if path.exists():
        try:
            with open(path, 'r') as f:
                bitacora = yaml.safe_load(f)
            validate_metadata(bitacora.get("metadata", {}))
            return bitacora
        except (yaml.YAMLError, ValueError) as e:
            raise RuntimeError(f"Error cargando bitácora: {str(e)}")
    
    # Estructura inicial si no existe
    return {
        "metadata": {
            "version": "0.2.0",
            "tipo": "bitacora",
            "schema": "almaresist.bitacora_v1",
            "descripcion": "Bitácora institucional de ALMA_RESIST",
            "estructura": "metadata + entradas",
            "tags": ["bitacora", "institucional"],
            "linked_to": [],
            "responsable": "Equipo de Operaciones",
            "hash_verificacion": "",
            "historial": [],
            "last_modified": datetime.now(timezone.utc).isoformat(),
            "last_modified_by": "system"
        },
        "entradas": []
    }

def create_backup(file_path):
    """Crea un backup con timestamp UTC"""
    backup_dir = Path(BACKUP_DIR).absolute()
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
    
    try:
        with open(file_path, 'rb') as src, open(backup_file, 'wb') as dst:
            dst.write(src.read())
        return backup_file
    except IOError as e:
        raise RuntimeError(f"Error creando backup: {str(e)}")

def calculate_file_hash(file_path):
    """Calcula hash SHA-256 de un archivo"""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return f"sha256:{sha256.hexdigest()}"
    except IOError as e:
        raise RuntimeError(f"Error calculando hash: {str(e)}")

# Funciones de generación de formatos
def save_triple_format(bitacora, base_path):
    """Guarda en triple formato: YAML, JSON y MD"""
    base_path = Path(base_path).absolute()
    parent_dir = base_path.parent
    parent_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar YAML (bitácora viva)
    yaml_path = base_path.with_suffix('.yaml')
    try:
        with open(yaml_path, 'w') as f:
            yaml.dump(bitacora, f, sort_keys=False, allow_unicode=True)
    except IOError as e:
        raise RuntimeError(f"Error guardando YAML: {str(e)}")
    
    # Guardar JSON
    json_path = base_path.with_suffix('.json')
    try:
        with open(json_path, 'w') as f:
            json.dump(bitacora, f, indent=2, ensure_ascii=False, default=str)
    except IOError as e:
        raise RuntimeError(f"Error guardando JSON: {str(e)}")
    
    # Guardar Markdown
    md_path = base_path.with_suffix('.md')
    try:
        with open(md_path, 'w') as f:
            # Front matter con metadatos
            f.write("---\n")
            yaml.dump(bitacora["metadata"], f, sort_keys=False, allow_unicode=True)
            f.write("---\n\n")
            
            # Cuerpo formateado
            f.write("# Bitácora Institucional\n\n")
            for entrada in bitacora["entradas"]:
                f.write(f"## {entrada['accion']} ({entrada['fecha']})\n")
                f.write(f"**ID**: `{entrada.get('id', '')}`  \n")
                f.write(f"**Ejecutado por**: {entrada['ejecutado_por']}  \n")
                f.write(f"**Estado**: {entrada.get('estado', 'registrado')}  \n\n")
                f.write(f"### Descripción\n{entrada['descripcion']}\n\n")
                f.write(f"### Motivo\n{entrada['motivo']}\n\n")
                if entrada.get('tags'):
                    f.write(f"**Tags**: {', '.join(entrada['tags'])}\n\n")
                f.write("---\n\n")
    except IOError as e:
        raise RuntimeError(f"Error guardando Markdown: {str(e)}")
    
    return yaml_path, json_path, md_path

# Función principal
def add_bitacora_entry(args):
    """Añade una nueva entrada a la bitácora"""
    logger = setup_logging(LOG_DIR if args.log else None, args.verbose)
    logger.info("Iniciando proceso de registro en bitácora")
    
    try:
        # Preparar nueva entrada
        new_entry = {
            "id": str(uuid.uuid4()),
            "fecha": datetime.now(timezone.utc).isoformat(),
            "accion": args.accion,
            "descripcion": args.descripcion,
            "motivo": args.motivo,
            "ejecutado_por": args.ejecutado_por,
            "estado": args.estado,
            "tags": args.tags.split(",") if args.tags else []
        }
        validate_entry(new_entry)
        
        # Cargar bitácora existente o crear nueva
        bitacora_path = Path(args.bitacora).absolute()
        bitacora = load_bitacora(bitacora_path)
        
        # Crear backup antes de modificar
        if not args.dry_run:
            backup_file = create_backup(bitacora_path)
            logger.info(f"Backup creado: {backup_file}")
        
        # Actualizar metadatos
        metadata = bitacora["metadata"]
        metadata["last_modified"] = new_entry["fecha"]
        metadata["last_modified_by"] = new_entry["ejecutado_por"]
        
        # Registrar en historial
        metadata["historial"].append({
            "fecha": new_entry["fecha"],
            "accion": "Nueva entrada",
            "ejecutado_por": new_entry["ejecutado_por"]
        })
        
        # Añadir nueva entrada
        bitacora["entradas"].append(new_entry)
        
        # Validar estructura completa
        validate_metadata(metadata)
        
        # Guardar en triple formato
        if not args.dry_run:
            yaml_path, json_path, md_path = save_triple_format(bitacora, bitacora_path)
            logger.info(f"Archivos generados:\n- YAML: {yaml_path}\n- JSON: {json_path}\n- MD: {md_path}")
            
            # Calcular y actualizar hash
            metadata["hash_verificacion"] = calculate_file_hash(yaml_path)
            save_triple_format(bitacora, bitacora_path)  # Guardar con hash actualizado
            
            logger.info(f"Entrada registrada exitosamente. ID: {new_entry['id']}")
            return True
        else:
            logger.info("Simulación completada (dry-run). No se realizaron cambios reales.")
            return True
            
    except Exception as e:
        logger.error(f"Error crítico: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI para gestión de bitácoras institucionales ALMA_RESIST",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Argumentos obligatorios
    parser.add_argument("--accion", required=True, help="Acción realizada")
    parser.add_argument("--descripcion", required=True, help="Descripción detallada de la acción")
    parser.add_argument("--motivo", required=True, help="Motivo de la acción")
    parser.add_argument("--ejecutado_por", required=True, help="Persona o sistema que ejecutó la acción")
    
    # Argumentos opcionales
    parser.add_argument("--bitacora", default=DEFAULT_BITACORA_PATH, 
                       help="Ruta al archivo principal de bitácora")
    parser.add_argument("--estado", default="registrado", choices=VALID_ESTADOS,
                       help="Estado actual de la acción")
    parser.add_argument("--tags", help="Etiquetas asociadas (separadas por comas)")
    
    # Flags de control
    parser.add_argument("--dry-run", action="store_true", 
                       help="Simula la ejecución sin realizar cambios")
    parser.add_argument("--verbose", action="store_true", 
                       help="Muestra información detallada del proceso")
    parser.add_argument("--log", action="store_true", 
                       help="Guarda registro detallado en archivo de logs")
    
    args = parser.parse_args()
    
    # Ejecutar proceso principal
    success = add_bitacora_entry(args)
    sys.exit(0 if success else 1)