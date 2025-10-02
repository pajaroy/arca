#!/usr/bin/env python3
"""
Cargador Robustecido de Memorias ALMA_RESIST v2.0
Características principales:
- Validación estricta de campos y formatos
- Manejo elegante de errores
- Compatibilidad con JSON/YAML
- Estadísticas detalladas
- Sistema de logging básico
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Any, Tuple, Set
from pathlib import Path

try:
    import yaml
except ImportError:
    print("✖ Falta pyyaml. Instalar con: pip install pyyaml")
    sys.exit(1)

# Configuración global
CAMPOS_OBLIGATORIOS = ['id', 'tipo', 'fecha', 'modulo', 'tema', 'status', 'responsable', 'tags', 'resumen']
LOG_PREFIXES = {
    'info': '[ℹ]',
    'success': '[✓]',
    'warning': '[!]',
    'error': '[✖]',
    'debug': '[DEBUG]'
}

def log(message: str, level: str = 'info') -> None:
    """Logging consistente para toda la aplicación"""
    print(f"{LOG_PREFIXES.get(level, LOG_PREFIXES['info'])} {message}")

def validar_formato_archivo(ruta: str) -> bool:
    """Verifica que el archivo tenga extensión válida y exista"""
    if not Path(ruta).exists():
        log(f"Archivo no encontrado: {ruta}", 'error')
        return False
    if not ruta.lower().endswith(('.json', '.yaml', '.yml')):
        log(f"Formato no soportado: {ruta}", 'error')
        return False
    return True

def cargar_archivo_seguro(ruta: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Carga archivos JSON/YAML con manejo robusto de errores
    Devuelve: (datos, errores)
    """
    errores = []
    datos = []
    
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
            
            if not contenido:
                errores.append("Archivo vacío")
                return datos, errores
                
            if ruta.endswith('.json'):
                datos = json.loads(contenido)
            else:  # YAML
                datos = yaml.safe_load(contenido) or []
                
    except json.JSONDecodeError as e:
        errores.append(f"JSON inválido: {str(e)}")
    except yaml.YAMLError as e:
        errores.append(f"YAML inválido: {str(e)}")
    except Exception as e:
        errores.append(f"Error inesperado: {str(e)}")
    
    return datos, errores

def validar_memoria(memoria: Dict[str, Any], idx: int) -> Tuple[bool, List[str]]:
    """Valida una memoria individual devolviendo (es_valida, errores)"""
    errores = []
    
    # Validación de campos obligatorios
    campos_faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if campo not in memoria]
    if campos_faltantes:
        errores.append(f"Campos obligatorios faltantes: {', '.join(campos_faltantes)}")
    
    # Validación básica de tipos
    if 'id' in memoria and not isinstance(memoria['id'], str):
        errores.append("El campo 'id' debe ser texto")
    
    if 'tags' in memoria and not isinstance(memoria['tags'], list):
        errores.append("El campo 'tags' debe ser una lista")
    
    return (len(errores) == 0, errores)

def procesar_memorias(nuevas_memorias: List[Dict[str, Any]], ids_existentes: Set[str]) -> Tuple[List[Dict[str, Any]], dict]:
    """
    Procesa memorias nuevas y devuelve:
    - memorias_validas: Lista de memorias que pasaron validación
    - estadisticas: Diccionario con conteo de operaciones
    """
    estadisticas = {
        'agregadas': 0,
        'duplicadas': 0,
        'invalidas': 0,
        'errores': []
    }
    memorias_validas = []
    
    for idx, memoria in enumerate(nuevas_memorias, 1):
        # Validación básica
        es_valida, errores = validar_memoria(memoria, idx)
        
        if not es_valida:
            estadisticas['invalidas'] += 1
            id_memoria = memoria.get('id', f"Registro #{idx}")
            for error in errores:
                estadisticas['errores'].append(f"{id_memoria}: {error}")
            continue
        
        # Verificación de duplicados
        if memoria['id'] in ids_existentes:
            estadisticas['duplicadas'] += 1
            log(f"Duplicado omitido: {memoria['id']}", 'warning')
            continue
        
        # Memoria válida
        memorias_validas.append(memoria)
        ids_existentes.add(memoria['id'])
        estadisticas['agregadas'] += 1
    
    return memorias_validas, estadisticas

def main():
    parser = argparse.ArgumentParser(
        description="Cargador Robustecido v2.0 de Memorias ALMA_RESIST",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Archivo de entrada con memorias (JSON/YAML)"
    )
    parser.add_argument(
        "--dest",
        required=True,
        help="Archivo destino (memorias.json/yaml o bitacora_viva.json/yaml)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostrar detalles de depuración"
    )
    
    args = parser.parse_args()
    
    # Validación inicial de archivos
    if not validar_formato_archivo(args.input):
        sys.exit(1)
    
    # Cargar memorias nuevas
    nuevas_memorias, errores_carga = cargar_archivo_seguro(args.input)
    if errores_carga:
        for error in errores_carga:
            log(f"Error cargando {args.input}: {error}", 'error')
        sys.exit(1)
    
    # Normalizar a lista si es un solo registro
    if isinstance(nuevas_memorias, dict):
        nuevas_memorias = [nuevas_memorias]
    
    # Cargar base existente
    memorias_existentes, _ = cargar_archivo_seguro(args.dest)
    ids_existentes = {m['id'] for m in memorias_existentes if 'id' in m}
    
    # Procesar memorias
    memorias_validas, stats = procesar_memorias(nuevas_memorias, ids_existentes)
    
    # Guardar resultados
    if memorias_validas:
        try:
            guardar_archivo_seguro(args.dest, memorias_existentes + memorias_validas)
        except Exception as e:
            log(f"Error guardando {args.dest}: {str(e)}", 'error')
            sys.exit(1)
    
    # Reporte final
    log("\nResumen de operación:", 'info')
    log(f"Memorias agregadas: {stats['agregadas']}", 'success')
    log(f"Duplicadas omitidas: {stats['duplicadas']}", 'warning')
    log(f"Invalidas rechazadas: {stats['invalidas']}", 'warning')
    
    if args.verbose and stats['errores']:
        log("\nDetalle de errores:", 'info')
        for error in stats['errores']:
            log(error, 'debug')

def guardar_archivo_seguro(ruta: str, datos: List[Dict[str, Any]]) -> None:
    """Guarda datos con manejo robusto de errores"""
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            if ruta.endswith('.json'):
                json.dump(datos, f, indent=2, ensure_ascii=False)
            else:  # YAML
                yaml.safe_dump(datos, f, allow_unicode=True, sort_keys=False)
    except Exception as e:
        raise Exception(f"Error guardando archivo: {str(e)}")

if __name__ == "__main__":
    main()