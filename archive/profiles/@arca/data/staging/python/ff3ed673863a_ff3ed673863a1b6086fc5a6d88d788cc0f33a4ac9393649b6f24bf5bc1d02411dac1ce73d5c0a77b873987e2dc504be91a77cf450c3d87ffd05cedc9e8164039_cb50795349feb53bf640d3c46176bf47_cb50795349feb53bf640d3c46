#!/usr/bin/env python3
# fix_metadata_v2.py - Script universal de corrección de metadatos para ALMA_RESIST

"""
📝 Script: fix_metadata_v2.py
🔖 ID: SCRIPT_2025-06-05_02
🛠️ Función: Validar, corregir y estandarizar metadatos en archivos críticos del ecosistema ALMA_RESIST
📚 Referencia: [IDEA_2025-06-06_01]
"""

import os
import sys
import re
import hashlib
import json
import argparse
import datetime
import shutil
import fnmatch
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set

# =====================================================================
# CONFIGURACIÓN GLOBAL
# =====================================================================
SUPPORTED_EXTENSIONS = {'.md', '.yaml', '.yml', '.json', '.py', '.sh'}
EXCLUDED_EXTENSIONS = {'.jpg', '.png', '.zip', '.db', '.mp4', '.exe', '.tmp', '.bak', '.lock'}
EXCLUDED_DIRS = {
    '.git', '.github', '.obsidian', 'venv', 'env', 'virtualenv', '__pycache__',
    'node_modules', 'datasets', 'data', 'media', 'images', 'img', 'bin',
    'backup', 'backups', 'logs', 'tmp', 'temp', 'core/scripts/fix_metadata'
}
MODULE_MARKER = "ALMA_RESIST"
SCRIPT_VERSION = "2.0"
ALMA_VERSION = "Centralesis v2.3"
IGNORE_FILE = ".fix_metadata_ignore"

# Colores para terminal
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

# =====================================================================
# FUNCIONES AUXILIARES
# =====================================================================

def load_ignore_patterns(root_path: Path) -> Set[str]:
    """Carga patrones de exclusión desde archivo .fix_metadata_ignore"""
    ignore_patterns = set()
    ignore_file = root_path / IGNORE_FILE
    
    if ignore_file.exists():
        with open(ignore_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.add(line)
    
    # Patrones predeterminados
    ignore_patterns.update([
        '*/.sync*', '*/.*', '*.sync-conflict-*'
    ])
    
    return ignore_patterns

def is_excluded(path: Path, exclude_dirs: Set[str], ignore_patterns: Set[str]) -> bool:
    """Determina si una ruta debe ser excluida del procesamiento"""
    # Exclusión por nombre de directorio
    for part in path.parts:
        if part in exclude_dirs:
            return True
    
    # Exclusión por extensión
    if path.suffix.lower() in EXCLUDED_EXTENSIONS:
        return True
    
    # Exclusión por patrón
    rel_path = str(path.relative_to(path.anchor))
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(path.name, pattern):
            return True
    
    return False

def find_module_root(start_path: Path) -> Path:
    """Busca recursivamente el directorio raíz del módulo ALMA_RESIST"""
    current_path = start_path.resolve()
    while current_path != current_path.parent:
        if current_path.name == MODULE_MARKER:
            return current_path
        current_path = current_path.parent
    
    raise FileNotFoundError(f"{COLOR_RED}No se encontró el directorio raíz del módulo {MODULE_MARKER}{COLOR_RESET}")

def extract_metadata(content: str) -> Tuple[Optional[Dict], str, bool]:
    """Extrae el bloque de metadatos YAML del contenido"""
    metadata_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(metadata_pattern, content, re.DOTALL)
    
    if match:
        try:
            metadata_str = match.group(1)
            rest_content = match.group(2)
            metadata = yaml.safe_load(metadata_str) if metadata_str else {}
            return (metadata or {}, rest_content, True)
        except Exception as e:
            return ({}, content, False)
    
    return ({}, content, False)

def calculate_content_hash(metadata: Dict, rest_content: str) -> str:
    """Calcula el hash SHA256 del contenido excluyendo el campo hash_integridad"""
    metadata_without_hash = metadata.copy()
    metadata_without_hash.pop('hash_integridad', None)
    
    reconstructed_content = (
        "---\n" +
        yaml.dump(metadata_without_hash, sort_keys=False) +
        "---\n" +
        rest_content
    )
    
    sha256 = hashlib.sha256()
    sha256.update(reconstructed_content.encode('utf-8'))
    return f"sha256:{sha256.hexdigest()}"

def generate_id(tipo: str, date_str: str, counter: int) -> str:
    """Genera un ID único según el estándar ALMA_RESIST"""
    return f"{tipo.upper()}_{date_str}_{counter:02d}"

def determine_file_type(file_path: Path) -> str:
    """Determina el tipo de archivo basado en su extensión y contenido"""
    ext = file_path.suffix.lower()
    content = file_path.read_text(encoding='utf-8', errors='ignore')[:500].lower()
    
    if ext == '.md':
        if 'changelog' in content:
            return 'changelog'
        if 'bitácora' in content or 'log' in content:
            return 'bitacora'
        return 'documento'
    elif ext in ['.py', '.sh']:
        return 'script'
    elif ext in ['.yaml', '.yml']:
        return 'configuracion'
    elif ext == '.json':
        return 'configuracion_json'
    return 'documento'

def normalize_metadata(metadata: Dict, file_path: Path, module_root: Path, counter: int) -> Tuple[Dict, Dict]:
    """Normaliza los metadatos según el estándar ALMA_RESIST"""
    changes = {}
    today = datetime.date.today().isoformat()
    rel_path = file_path.relative_to(module_root.parent if module_root.name == MODULE_MARKER else module_root)
    module_name = rel_path.parts[0] if rel_path.parts else "desconocido"
    
    # Determinar tipo de archivo
    current_type = metadata.get('tipo', '').lower()
    valid_types = {'fundacional', 'decision', 'bitacora', 'changelog', 'script', 'configuracion', 'configuracion_json'}
    
    if not current_type or current_type not in valid_types:
        new_type = determine_file_type(file_path)
        if current_type != new_type:
            changes['tipo'] = {'old': current_type, 'new': new_type}
            metadata['tipo'] = new_type
    
    # Generar/actualizar ID
    if not metadata.get('id') or not re.match(r'^[A-Z]+_\d{4}-\d{2}-\d{2}_\d{2}$', metadata['id']):
        new_id = generate_id(metadata['tipo'], today, counter)
        changes['id'] = {'old': metadata.get('id'), 'new': new_id}
        metadata['id'] = new_id
    
    # Campos obligatorios con valores por defecto
    defaults = {
        'version': '1.0',
        'formato': file_path.suffix[1:],
        'modulo': module_name,
        'titulo': file_path.stem.replace('_', ' ').title(),
        'autor': os.getlogin(),
        'fecha_creacion': today,
        'fecha_actualizacion': today,
        'status': 'activo',
        'version_sistema': ALMA_VERSION,
        'origen': 'automatico',
        'tags': [],
        'linked_to': [],
        'descripcion': 'Documento procesado automáticamente'
    }
    
    for field, default in defaults.items():
        current_val = metadata.get(field)
        if not current_val:
            changes[field] = {'old': current_val, 'new': default}
            metadata[field] = default
    
    # Actualizar fecha de actualización
    if 'fecha_actualizacion' not in changes:
        changes['fecha_actualizacion'] = {'old': metadata.get('fecha_actualizacion'), 'new': today}
    metadata['fecha_actualizacion'] = today
    
    return metadata, changes

def safe_write_file(file_path: Path, content: str, backup_path: Path) -> bool:
    """Escribe un archivo de forma segura con rollback automático"""
    try:
        # Crear backup
        shutil.copy2(file_path, backup_path)
        
        # Intentar escribir el nuevo contenido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        # Restaurar desde backup en caso de error
        try:
            shutil.copy2(backup_path, file_path)
            os.remove(backup_path)
        except Exception:
            pass
        raise e

def process_file(file_path: Path, module_root: Path, dry_run: bool, log_file: Path, counter: int) -> Dict:
    """Procesa un archivo individual"""
    result = {
        'file': str(file_path),
        'timestamp': datetime.datetime.now().isoformat(),
        'action': 'skipped',
        'changes': {},
        'backup': None,
        'error': None
    }
    
    try:
        # Leer contenido
        content = file_path.read_text(encoding='utf-8')
        metadata, rest_content, has_metadata = extract_metadata(content)
        
        # Normalizar metadatos
        new_metadata, changes = normalize_metadata(metadata, file_path, module_root, counter)
        result['changes'] = changes
        
        # Calcular hash
        new_metadata['hash_integridad'] = calculate_content_hash(new_metadata, rest_content)
        
        # Construir nuevo contenido
        new_metadata_block = yaml.dump(new_metadata, sort_keys=False, allow_unicode=True)
        new_content = f"---\n{new_metadata_block}---\n{rest_content}"
        
        # Verificar si hay cambios
        if new_content == content and has_metadata:
            result['action'] = 'no_change'
            return result
        
        # Preparar backup
        backup_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = file_path.with_name(f"{file_path.stem}_{backup_time}.bak")
        result['backup'] = str(backup_path)
        
        # Modo dry-run
        if dry_run:
            result['action'] = 'simulated_update'
            return result
        
        # Escribir cambios (con rollback automático)
        safe_write_file(file_path, new_content, backup_path)
        result['action'] = 'updated' if has_metadata else 'created'
        
    except Exception as e:
        result['error'] = str(e)
        result['action'] = 'error'
    
    # Registrar en log
    if log_file:
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    return result

def print_summary(stats: Dict):
    """Muestra un resumen colorizado del proceso"""
    processed = stats['processed']
    modified = stats['modified']
    errors = stats['errors']
    skipped = stats['skipped']
    warnings = stats['warnings']
    
    print(f"\n{'='*50}")
    print(f"{COLOR_BLUE}📊 RESUMEN DEL PROCESO{COLOR_RESET}")
    print(f"{'='*50}")
    print(f"• Archivos procesados: {COLOR_BLUE}{processed}{COLOR_RESET}")
    print(f"• Archivos modificados: {COLOR_GREEN}{modified}{COLOR_RESET}")
    print(f"• Archivos saltados: {COLOR_YELLOW}{skipped}{COLOR_RESET}")
    print(f"• Advertencias: {COLOR_YELLOW}{warnings}{COLOR_RESET}")
    print(f"• Errores: {COLOR_RED if errors > 0 else COLOR_BLUE}{errors}{COLOR_RESET}")
    print(f"{'='*50}")
    
    if errors > 0:
        print(f"\n{COLOR_RED}❌ PROCESO FINALIZADO CON ERRORES{COLOR_RESET}")
        print(f"Revisa el log para detalles: {stats['log_file']}")
        sys.exit(1)
    elif warnings > 0 or skipped > 0:
        print(f"\n{COLOR_YELLOW}⚠️ PROCESO FINALIZADO CON ADVERTENCIAS{COLOR_RESET}")
        print(f"Algunos archivos no pudieron procesarse automáticamente")
        print(f"Revisa el log para detalles: {stats['log_file']}")
    else:
        print(f"\n{COLOR_GREEN}✅ PROCESO COMPLETADO CORRECTAMENTE{COLOR_RESET}")
        print(f"Todos los archivos procesados sin errores")

def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(
        description='Herramienta de normalización de metadatos ALMA_RESIST v2',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--dry-run', action='store_true', help='Simular cambios sin modificar archivos')
    parser.add_argument('--log-file', default='fix_metadata.log', help='Ruta del archivo de registro')
    parser.add_argument('--root-dir', help='Directorio raíz del módulo (autodetectado por defecto)')
    parser.add_argument('--exclude', nargs='+', default=[], help='Patrones adicionales de exclusión')
    args = parser.parse_args()
    
    # Configuración inicial
    script_dir = Path(__file__).parent
    log_path = script_dir / args.log_file
    
    # Estadísticas
    stats = {
        'processed': 0,
        'modified': 0,
        'skipped': 0,
        'errors': 0,
        'warnings': 0,
        'log_file': str(log_path)
    }
    
    try:
        # Inicializar log
        if log_path.exists():
            backup_log = log_path.with_name(f"{log_path.stem}_backup{log_path.suffix}")
            shutil.copy2(log_path, backup_log)
        
        # Determinar raíz del módulo
        module_root = find_module_root(script_dir) if not args.root_dir else Path(args.root_dir)
        print(f"{COLOR_BLUE}📂 Módulo identificado: {module_root}{COLOR_RESET}")
        
        # Cargar patrones de exclusión
        exclude_dirs = EXCLUDED_DIRS.copy()
        ignore_patterns = load_ignore_patterns(module_root)
        ignore_patterns.update(args.exclude)
        
        # Recorrer archivos
        for root, dirs, files in os.walk(module_root, topdown=True):
            # Excluir directorios
            dirs[:] = [d for d in dirs if not is_excluded(Path(root) / d, exclude_dirs, ignore_patterns)]
            
            for file in files:
                file_path = Path(root) / file
                
                # Verificar si está excluido
                if is_excluded(file_path, exclude_dirs, ignore_patterns):
                    stats['skipped'] += 1
                    continue
                
                # Verificar extensión soportada
                if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    stats['skipped'] += 1
                    continue
                
                # Procesar archivo
                stats['processed'] += 1
                result = process_file(
                    file_path, 
                    module_root,
                    args.dry_run,
                    log_path,
                    stats['processed']
                )
                
                # Actualizar estadísticas
                if result['action'] in ['updated', 'created']:
                    stats['modified'] += 1
                elif result['action'] == 'error':
                    stats['errors'] += 1
                elif result['action'] == 'skipped':
                    stats['skipped'] += 1
                elif result['changes']:
                    stats['warnings'] += 1
                
                # Mostrar estado
                status_color = COLOR_GREEN
                if result['action'] == 'error':
                    status_color = COLOR_RED
                elif result['action'] in ['skipped', 'no_change']:
                    status_color = COLOR_YELLOW
                
                print(f"{status_color}{result['action'][0].upper()}{COLOR_RESET} {file_path}")
        
        # Mostrar resumen
        print_summary(stats)
        
    except Exception as e:
        print(f"{COLOR_RED}⛔ ERROR CRÍTICO: {str(e)}{COLOR_RESET}")
        sys.exit(1)

# =====================================================================
# INICIALIZACIÓN
# =====================================================================
if __name__ == "__main__":
    try:
        import yaml
    except ImportError:
        print(f"{COLOR_RED}✋ Error: Se requiere PyYAML. Instale con: pip install PyYAML{COLOR_RESET}")
        sys.exit(1)
    
    main()