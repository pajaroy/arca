"""
---
metadatos:
  id_unico: "scr-py-004"
  tipo: "utilidad"
  nombre: "import_validate_schemas.py"
  version: "0.1.0"
  estado: "archivado"
  dependencias: ["validate_schemas.py"]
  descripcion: "Script para validar y completar bloques de frontmatter en archivos del ecosistema ARCA."
---
"""

#!/usr/bin/env python3
#El script se adapta dinámicamente a los formatos y delimitadores definidos en config.yaml,
#permitiendo agregar nuevos formatos sin modificar el código.

import os
import re
import json
import yaml
import hashlib
from typing import List, Dict, Optional, Union, Any
from pathlib import Path

# Importaciones de configuración y utilidades
from load_config import CONFIG
from validate_schemas import validar_schemas
from logger import logger

class FrontmatterValidator:
    """Clase principal para validar y completar frontmatter en archivos."""
    
    def __init__(self):
        """Inicializa el validador cargando configuración desde CONFIG."""
        self.schema = CONFIG.get('metadatos_frontmatter', {})
        self.formatos_soportados = CONFIG.get('formatos_soportados', {})
        self.required_fields = self.schema.get('required', [])
        self.recommended_fields = self.schema.get('recommended', [])
        
        # Validar configuración de formatos
        if not self.formatos_soportados:
            logger.error("No se encontraron formatos soportados en config.yaml")
            raise ValueError("Configuración incompleta: formatos_soportados")
        
    def calcular_hash(self, contenido: str) -> str:
        """Calcula el hash SHA-256 del contenido del archivo."""
        return hashlib.sha256(contenido.encode('utf-8')).hexdigest()
    
    def detectar_formato(self, filepath: str) -> Optional[str]:
        """
        Detecta el formato del archivo basado en su extensión usando config.yaml.
        
        Args:
            filepath: Ruta al archivo a verificar
            
        Returns:
            str: Clave del formato en config.yaml si es soportado, None en caso contrario
        """
        ext = Path(filepath).suffix[1:].lower()
        return next(
            (fmt for fmt, config in self.formatos_soportados.items() 
             if ext in config.get('extensiones', [])),
            None
        )
    
    def extraer_frontmatter(self, filepath: str, formato: str) -> tuple:
        """
        Extrae el frontmatter del archivo si existe, según la configuración del formato.
        
        Args:
            filepath: Ruta al archivo
            formato: Clave del formato en config.yaml
            
        Returns:
            tuple: (frontmatter_dict, contenido_restante, posicion_inicio, posicion_fin)
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        config_formato = self.formatos_soportados.get(formato, {})
        delimitador = config_formato.get('delimitador', '')
        delimitador_fin = config_formato.get('delimitador_fin', delimitador)
        tipo = config_formato.get('tipo', 'yaml')
        
        # Determinar parser según tipo
        parser = yaml.safe_load if tipo == 'yaml' else json.loads
        
        # Construir patrón regex según configuración
        if tipo == 'yaml':
            pattern = rf'^{delimitador}(.*?){delimitador_fin}(.*)'
        elif tipo == 'json':
            pattern = r'^\s*(\{.*?\})\s*(.*)'
        else:
            logger.warning(f"Tipo de frontmatter no soportado: {tipo}")
            return None, contenido, 0, 0
        
        match = re.match(pattern, contenido, re.DOTALL)
        
        if not match:
            return None, contenido, 0, 0
        
        try:
            frontmatter = parser(match.group(1).strip())
            return (
                frontmatter,
                match.group(2),
                match.start(1),
                match.end(1)
            )
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            logger.warning(f"Frontmatter mal formado en {filepath}: {str(e)}")
            return None, contenido, 0, 0
    
    def validar_frontmatter(self, frontmatter: dict) -> dict:
        """
        Valida el frontmatter contra el schema definido en config.yaml.
        
        Args:
            frontmatter: Diccionario con los metadatos a validar
            
        Returns:
            dict: Resultados de validación con estructura:
                {
                    'valid': bool,
                    'missing_required': list,
                    'missing_recommended': list,
                    'invalid_fields': dict
                }
        """
        resultado = {
            'valid': True,
            'missing_required': [],
            'missing_recommended': [],
            'invalid_fields': {}
        }
        
        # Validar campos requeridos
        for field in self.required_fields:
            if field not in frontmatter:
                resultado['missing_required'].append(field)
                resultado['valid'] = False
        
        # Validar campos recomendados
        for field in self.recommended_fields:
            if field not in frontmatter:
                resultado['missing_recommended'].append(field)
        
        # Validación adicional con el schema completo
        schema_validation = validar_schemas(frontmatter, self.schema)
        if not schema_validation['valid']:
            resultado['valid'] = False
            resultado['invalid_fields'] = schema_validation.get('errors', {})
        
        return resultado
    
    def generar_frontmatter_base(self) -> dict:
        """Genera un frontmatter base con los campos mínimos requeridos."""
        frontmatter = {}
        for field in self.required_fields:
            frontmatter[field] = self.schema['properties'].get(field, {}).get('default', '')
        return frontmatter
    
    def completar_frontmatter(self, existing: dict) -> dict:
        """Completa un frontmatter existente con campos faltantes."""
        frontmatter = existing.copy()
        
        # Agregar campos requeridos faltantes
        for field in self.required_fields:
            if field not in frontmatter:
                frontmatter[field] = self.schema['properties'].get(field, {}).get('default', '')
        
        # Agregar campos recomendados faltantes
        for field in self.recommended_fields:
            if field not in frontmatter:
                frontmatter[field] = self.schema['properties'].get(field, {}).get('default', '')
        
        return frontmatter
    
    def formatear_frontmatter(self, frontmatter: dict, formato: str) -> str:
        """
        Formatea el frontmatter según la configuración del formato.
        
        Args:
            frontmatter: Diccionario con los metadatos
            formato: Clave del formato en config.yaml
            
        Returns:
            str: Frontmatter formateado según el tipo de archivo
        """
        config_formato = self.formatos_soportados.get(formato, {})
        tipo = config_formato.get('tipo', 'yaml')
        delimitador = config_formato.get('delimitador', '')
        delimitador_fin = config_formato.get('delimitador_fin', delimitador)
        
        if tipo == 'yaml':
            yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
            return f"{delimitador}{yaml_str}{delimitador_fin}"
        elif tipo == 'json':
            return json.dumps(frontmatter, indent=2)
        else:
            logger.warning(f"Tipo de frontmatter no soportado para formateo: {tipo}")
            return ""
    
    def procesar_archivo(self, filepath: str) -> bool:
        """
        Procesa un archivo individual validando y completando su frontmatter.
        
        Args:
            filepath: Ruta al archivo a procesar
            
        Returns:
            bool: True si se modificó el archivo, False en caso contrario
        """
        formato = self.detectar_formato(filepath)
        if not formato:
            logger.debug(f"Formato no soportado: {filepath}")
            return False
        
        frontmatter, contenido, inicio, fin = self.extraer_frontmatter(filepath, formato)
        hash_original = self.calcular_hash(contenido)
        
        # Si no hay frontmatter, crear uno nuevo
        if frontmatter is None:
            nuevo_frontmatter = self.generar_frontmatter_base()
            frontmatter_str = self.formatear_frontmatter(nuevo_frontmatter, formato)
            nuevo_contenido = f"{frontmatter_str}\n{contenido}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            
            logger.info(
                f"Archivo: {filepath} | Cambio: NUEVO | "
                f"Hash: {self.calcular_hash(nuevo_contenido)}"
            )
            return True
        
        # Validar el frontmatter existente
        validacion = self.validar_frontmatter(frontmatter)
        
        if validacion['valid'] and not validacion['missing_recommended']:
            logger.debug(f"Frontmatter válido en {filepath}")
            return False
        
        # Corregir frontmatter si es necesario
        frontmatter_corregido = self.completar_frontmatter(frontmatter)
        frontmatter_str = self.formatear_frontmatter(frontmatter_corregido, formato)
        
        # Reconstruir contenido
        if self.formatos_soportados[formato].get('tipo') == 'json':
            nuevo_contenido = f"{frontmatter_str}\n{contenido}"
        else:
            nuevo_contenido = contenido[:inicio] + frontmatter_str + contenido[fin:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        cambio_tipo = "CORREGIDO" if frontmatter else "COMPLETADO"
        logger.info(
            f"Archivo: {filepath} | Cambio: {cambio_tipo} | "
            f"Hash: {self.calcular_hash(nuevo_contenido)} | "
            f"Campos faltantes: {validacion['missing_required'] + validacion['missing_recommended']}"
        )
        return True
    
    def sugerir_mejoras_schema(self) -> List[str]:
        """Analiza el schema actual y sugiere posibles mejoras."""
        sugerencias = []
        
        if not self.required_fields:
            sugerencias.append("El schema no define campos requeridos (required)")
        
        if not self.recommended_fields:
            sugerencias.append("El schema no define campos recomendados (recommended)")
        
        campos_esenciales = ['id_unico', 'tipo', 'version', 'fecha_creacion']
        for campo in campos_esenciales:
            if campo not in self.required_fields + self.recommended_fields:
                sugerencias.append(f"Considerar agregar '{campo}' como campo requerido o recomendado")
        
        return sugerencias
    
    def procesar_ruta(self, ruta: Union[str, List[str]], recursivo: bool = False) -> Dict[str, int]:
        """
        Procesa una ruta o lista de rutas.
        
        Args:
            ruta: Puede ser un string con la ruta o una lista de rutas
            recursivo: Si es True, procesa subdirectorios recursivamente
            
        Returns:
            dict: Estadísticas de procesamiento {
                'archivos_procesados': int,
                'archivos_modificados': int,
                'archivos_omitidos': int
            }
        """
        stats = {
            'archivos_procesados': 0,
            'archivos_modificados': 0,
            'archivos_omitidos': 0
        }
        
        if isinstance(ruta, str):
            rutas = [ruta]
        else:
            rutas = ruta
        
        archivos_a_procesar = set()
        
        for ruta in rutas:
            if os.path.isfile(ruta):
                archivos_a_procesar.add(ruta)
            elif os.path.isdir(ruta):
                for root, _, files in os.walk(ruta):
                    for file in files:
                        if self.detectar_formato(file):
                            archivos_a_procesar.add(os.path.join(root, file))
                    if not recursivo:
                        break
        
        for archivo in archivos_a_procesar:
            stats['archivos_procesados'] += 1
            try:
                modificado = self.procesar_archivo(archivo)
                if modificado:
                    stats['archivos_modificados'] += 1
                else:
                    stats['archivos_omitidos'] += 1
            except Exception as e:
                logger.error(f"Error procesando {archivo}: {str(e)}")
                stats['archivos_omitidos'] += 1
        
        return stats

def main():
    """Función principal para ejecución como CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validador y completador de frontmatter para archivos ARCA"
    )
    parser.add_argument(
        'rutas', 
        nargs='+',
        help='Rutas a archivos o directorios a procesar'
    )
    parser.add_argument(
        '-r', '--recursivo',
        action='store_true',
        help='Procesar subdirectorios recursivamente'
    )
    parser.add_argument(
        '-s', '--sugerir-mejoras',
        action='store_true',
        help='Mostrar sugerencias para mejorar el schema'
    )
    
    args = parser.parse_args()
    
    validator = FrontmatterValidator()
    
    if args.sugerir_mejoras:
        sugerencias = validator.sugerir_mejoras_schema()
        if sugerencias:
            print("Sugerencias para mejorar schema.yaml:")
            for sug in sugerencias:
                print(f"- {sug}")
        else:
            print("El schema parece estar completo. No se encontraron sugerencias.")
        return
    
    stats = validator.procesar_ruta(args.rutas, args.recursivo)
    
    print("\nResumen de ejecución:")
    print(f"Archivos procesados: {stats['archivos_procesados']}")
    print(f"Archivos modificados: {stats['archivos_modificados']}")
    print(f"Archivos omitidos: {stats['archivos_omitidos']}")

if __name__ == '__main__':
    main()