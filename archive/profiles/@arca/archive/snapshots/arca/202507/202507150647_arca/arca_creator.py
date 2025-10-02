#!/usr/bin/env python3
"""
---
metadatos:
  id_unico: "scr-py-007"
  tipo: "core"
  nombre: "arca_creator.py"
  version: "0.1.0"
  estado: "activo"
  dependencias: []
  descripcion: "creador de archivos con encabezado y hash"
---

Script para crear archivos nuevos en el ecosistema ARCA con frontmatter válido.

Este módulo permite generar archivos con metadatos estructurados según la configuración
del sistema ARCA, incluyendo campos obligatorios, UUID, hash de integridad y marcas
temporales. Soporta múltiples formatos de archivo definidos en la configuración.
"""

import argparse
from datetime import datetime
import hashlib
from pathlib import Path
import uuid
from typing import Dict, Any, Optional

from load_config import CONFIG
from validate_schemas import validar_schemas
from logger import logger


def generar_uuid() -> str:
    """
    Genera un UUID según el algoritmo configurado en CONFIG.

    Returns:
        str: UUID generado según el algoritmo especificado en la configuración.

    Raises:
        ValueError: Si el algoritmo especificado no es soportado.
    """
    algoritmo = CONFIG['uuid_algorithm'].lower()
    
    if algoritmo == 'uuid1':
        return str(uuid.uuid1())
    elif algoritmo == 'uuid4':
        return str(uuid.uuid4())
    elif algoritmo == 'uuid3':
        # Usamos un namespace DNS y el timestamp actual como nombre
        namespace = uuid.NAMESPACE_DNS
        nombre = str(datetime.now().timestamp()).encode('utf-8')
        return str(uuid.uuid3(namespace, nombre))
    elif algoritmo == 'uuid5':
        # Similar a uuid3 pero con algoritmo SHA-1
        namespace = uuid.NAMESPACE_DNS
        nombre = str(datetime.now().timestamp()).encode('utf-8')
        return str(uuid.uuid5(namespace, nombre))
    else:
        error_msg = f"Algoritmo UUID no soportado: {algoritmo}"
        logger.error(error_msg)
        raise ValueError(error_msg)


def calcular_hash_integridad(contenido: str) -> str:
    """
    Calcula el hash de integridad para el contenido del archivo.

    Args:
        contenido (str): Contenido del archivo a hashear.

    Returns:
        str: Hash calculado según el algoritmo configurado.

    Raises:
        ValueError: Si el algoritmo de hash no es soportado.
    """
    algoritmo = CONFIG['hash_algorithm'].lower()
    contenido_bytes = contenido.encode('utf-8')
    
    if algoritmo == 'md5':
        return hashlib.md5(contenido_bytes).hexdigest()
    elif algoritmo == 'sha1':
        return hashlib.sha1(contenido_bytes).hexdigest()
    elif algoritmo == 'sha256':
        return hashlib.sha256(contenido_bytes).hexdigest()
    elif algoritmo == 'sha512':
        return hashlib.sha512(contenido_bytes).hexdigest()
    else:
        error_msg = f"Algoritmo hash no soportado: {algoritmo}"
        logger.error(error_msg)
        raise ValueError(error_msg)


def generar_frontmatter(tipo_archivo: str, nombre: str, autor: Optional[str] = None, 
                      descripcion: Optional[str] = None) -> Dict[str, Any]:
    """
    Genera el frontmatter con los metadatos obligatorios y opcionales.

    Args:
        tipo_archivo (str): Tipo de archivo (ej. 'csv', 'yaml').
        nombre (str): Nombre base del archivo.
        autor (str, optional): Autor del archivo. Defaults to None.
        descripcion (str, optional): Descripción del archivo. Defaults to None.

    Returns:
        Dict[str, Any]: Diccionario con todos los metadatos del frontmatter.
    """
    fecha_actual = datetime.now().isoformat()
    frontmatter = {
        'uuid': generar_uuid(),
        'fecha_creacion': fecha_actual,
        'fecha_modificacion': fecha_actual,
        'tipo_archivo': tipo_archivo,
        'nombre': nombre,
        **CONFIG['campos_obligatorios']
    }
    
    if autor:
        frontmatter['autor'] = autor
    if descripcion:
        frontmatter['descripcion'] = descripcion
    
    return frontmatter


def formatear_contenido(tipo_archivo: str, frontmatter: Dict[str, Any], 
                       contenido: Optional[str] = None) -> str:
    """
    Formatea el contenido del archivo con el frontmatter según el tipo de archivo.

    Args:
        tipo_archivo (str): Tipo de archivo (ej. 'csv', 'yaml').
        frontmatter (Dict[str, Any]): Metadatos a incluir en el frontmatter.
        contenido (str, optional): Contenido principal del archivo. Defaults to None.

    Returns:
        str: Contenido completo del archivo formateado.

    Raises:
        ValueError: Si el tipo de archivo no es soportado.
    """
    formato = CONFIG['formatos_soportados'].get(tipo_archivo)
    if not formato:
        error_msg = f"Tipo de archivo no soportado: {tipo_archivo}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    delimitador_inicio = formato['delimitador_inicio']
    delimitador_fin = formato['delimitador_fin']
    plantilla = formato.get('plantilla', '')
    
    # Convertir frontmatter a formato YAML para el bloque
    frontmatter_yaml = '\n'.join(f"{k}: {v}" for k, v in frontmatter.items())
    
    contenido_principal = contenido or plantilla
    archivo_completo = (
        f"{delimitador_inicio}\n"
        f"{frontmatter_yaml}\n"
        f"{delimitador_fin}\n"
        f"{contenido_principal}"
    )
    
    return archivo_completo


def generar_ruta_archivo(tipo_archivo: str, nombre: str) -> Path:
    """
    Genera la ruta absoluta para el nuevo archivo.

    Args:
        tipo_archivo (str): Tipo de archivo (ej. 'csv', 'yaml').
        nombre (str): Nombre base del archivo.

    Returns:
        Path: Ruta absoluta al nuevo archivo.

    Raises:
        ValueError: Si la extensión no es soportada.
    """
    if tipo_archivo not in CONFIG['formatos_soportados']:
        error_msg = f"Tipo de archivo no soportado: {tipo_archivo}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    base_path = Path(CONFIG['base_path'])
    nombre_archivo = f"{nombre}.{tipo_archivo}"
    ruta_archivo = base_path / nombre_archivo
    
    # Verificar si el archivo ya existe
    if ruta_archivo.exists():
        error_msg = f"El archivo ya existe: {ruta_archivo}"
        logger.error(error_msg)
        raise FileExistsError(error_msg)
    
    return ruta_archivo


def crear_archivo_arca(tipo_archivo: str, nombre: str, autor: Optional[str] = None, 
                      descripcion: Optional[str] = None, contenido: Optional[str] = None) -> Path:
    """
    Crea un nuevo archivo en el ecosistema ARCA con frontmatter válido.

    Args:
        tipo_archivo (str): Tipo de archivo (ej. 'csv', 'yaml').
        nombre (str): Nombre base del archivo.
        autor (str, optional): Autor del archivo. Defaults to None.
        descripcion (str, optional): Descripción del archivo. Defaults to None.
        contenido (str, optional): Contenido principal del archivo. Defaults to None.

    Returns:
        Path: Ruta al archivo creado.

    Raises:
        ValueError: Si hay problemas con los parámetros o validación.
        FileExistsError: Si el archivo ya existe.
    """
    try:
        # Generar metadatos
        frontmatter = generar_frontmatter(tipo_archivo, nombre, autor, descripcion)
        
        # Formatear contenido completo
        contenido_completo = formatear_contenido(tipo_archivo, frontmatter, contenido)
        
        # Calcular hash de integridad
        frontmatter['hash_integridad'] = calcular_hash_integridad(contenido_completo)
        
        # Regenerar contenido con el hash incluido
        contenido_completo = formatear_contenido(tipo_archivo, frontmatter, contenido)
        
        # Validar esquema
        if not validar_schemas(frontmatter):
            error_msg = "El frontmatter generado no cumple con el esquema definido"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Generar ruta y escribir archivo
        ruta_archivo = generar_ruta_archivo(tipo_archivo, nombre)
        ruta_archivo.write_text(contenido_completo, encoding='utf-8')
        
        logger.info(f"Archivo creado exitosamente: {ruta_archivo}")
        return ruta_archivo
    
    except Exception as e:
        logger.error(f"Error al crear archivo ARCA: {str(e)}")
        raise


def main():
    """Función principal para el uso desde CLI."""
    parser = argparse.ArgumentParser(
        description="Crea archivos nuevos en el ecosistema ARCA con frontmatter válido."
    )
    parser.add_argument(
        'tipo_archivo',
        type=str,
        help="Tipo de archivo a crear (ej. csv, yaml)"
    )
    parser.add_argument(
        'nombre',
        type=str,
        help="Nombre base del archivo (sin extensión)"
    )
    parser.add_argument(
        '--autor',
        type=str,
        required=False,
        help="Autor del archivo (opcional)"
    )
    parser.add_argument(
        '--descripcion',
        type=str,
        required=False,
        help="Descripción del archivo (opcional)"
    )
    
    args = parser.parse_args()
    
    try:
        ruta_archivo = crear_archivo_arca(
            tipo_archivo=args.tipo_archivo,
            nombre=args.nombre,
            autor=args.autor,
            descripcion=args.descripcion
        )
        print(f"Archivo creado exitosamente: {ruta_archivo}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == '__main__':
    main()