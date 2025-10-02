#!/usr/bin/env python3
# ~/@arca/source/main.py
# Version: 0.3.0
# Descripcion: Script para clasificar archivos por formato con mejoras de rendimiento y portabilidad
# Cambios principales:
#   - Configuración desde YAML
#   - Paralelismo para procesamiento
#   - Detección de duplicados en Python puro
#   - Mejor manejo de errores
#   - Uso de pathlib para rutas
#   - Metadatos con dataclasses

import os
import hashlib
import shutil
import yaml
from datetime import datetime
from pathlib import Path
import sys
from multiprocessing import Pool, cpu_count
from dataclasses import dataclass, asdict
import time

#################################################################################################################
# Configuración desde YAML
class Config:
    """Carga la configuración desde un archivo YAML."""
    
    def __init__(self, config_path="~/@arca/config.yaml"):
        self.config_path = Path(config_path).expanduser()
        self._load_config()
        self._create_directories()
    
    def _load_config(self):
        """Carga la configuración desde el archivo YAML."""
        try:
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Archivo de configuración no encontrado en {self.config_path}")
            sys.exit(1)
        
        self.root = Path(config_data['root']).expanduser()
        self.formats = config_data['formats']
        self.metadata_fields = config_data['metadata_fields']
        
        # Construir rutas
        paths = config_data['paths']
        self.raw_dir = self.root / paths['raw']
        self.staging_dir = self.root / paths['staging']
        self.log_file = self.root / paths['log_file']
        self.database_file = self.root / paths['database_file']
    
    def _create_directories(self):
        """Crea los directorios necesarios si no existen."""
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        for format_dir in self.formats:
            (self.staging_dir / format_dir).mkdir(parents=True, exist_ok=True)

#################################################################################################################
# Clasificador de archivos
class FileClassifier:
    """Clasifica archivos por su extensión."""
    
    def __init__(self, config):
        self.config = config
    
    def get_file_type(self, file_path: Path) -> str:
        """Determina el tipo de archivo basado en su extensión."""
        ext = file_path.suffix.lower().lstrip('.')
        
        if ext in self.config.formats:
            return ext
        elif ext in ['txt', 'md', 'markdown']:
            return 'markdown'
        elif ext in ['py']:
            return 'python'
        else:
            return 'otros'
    
    def classify_files(self) -> list:
        """Recorre recursivamente el directorio raw y clasifica los archivos."""
        classified_files = []
        
        for file_path in self.config.raw_dir.rglob('*'):
            if file_path.is_file():
                file_type = self.get_file_type(file_path)
                classified_files.append((file_path, file_type))
        
        return classified_files

#################################################################################################################
# Manejo de Hash con caché
class HashManager:
    """Calcula y cachea hashes de archivos."""
    
    def __init__(self):
        self.hash_cache = {}
    
    def calculate_blake3(self, file_path: Path) -> str:
        """Calcula el hash Blake2b de un archivo (con caché)."""
        if file_path in self.hash_cache:
            return self.hash_cache[file_path]
        
        hasher = hashlib.blake2b()
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        
        hash_value = hasher.hexdigest()
        self.hash_cache[file_path] = hash_value
        return hash_value

#################################################################################################################
# Detección de duplicados en Python puro
class DupesFinder:
    """Encuentra duplicados exactos comparando hashes."""
    
    def __init__(self, config):
        self.config = config
    
    def find_duplicates(self, directory: Path) -> list:
        """Busca archivos duplicados en un directorio."""
        file_hashes = {}
        
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                hasher = hashlib.blake2b()
                with open(file_path, 'rb') as f:
                    while chunk := f.read(8192):
                        hasher.update(chunk)
                file_hash = hasher.hexdigest()
                file_hashes.setdefault(file_hash, []).append(file_path)
        
        return [group for group in file_hashes.values() if len(group) > 1]
    
    def handle_duplicates(self, directory: Path, keep_in: str = 'staging'):
        """Elimina duplicados, conservando solo una copia."""
        duplicate_groups = self.find_duplicates(directory)
        
        for group in duplicate_groups:
            # Conservar el primer archivo del grupo
            original = group[0]
            
            for duplicate in group[1:]:
                try:
                    # Solo eliminar si está en raw (después de mover) o según política
                    if keep_in == 'staging' and duplicate.parent == self.config.raw_dir:
                        duplicate.unlink()
                    elif keep_in == 'raw' and duplicate.parent != self.config.raw_dir:
                        duplicate.unlink()
                    else:
                        # Por defecto: eliminar duplicados en raw
                        if duplicate.parent == self.config.raw_dir:
                            duplicate.unlink()
                except Exception as e:
                    print(f"Error eliminando duplicado {duplicate}: {str(e)}")

#################################################################################################################
# Database y Logging
@dataclass
class FileMetadata:
    """Estructura para los metadatos de archivos."""
    ruta: Path
    nombre: str
    tipo: str
    tamano_bytes: int
    fecha_mod: str
    hash_blake3: str
    contenido: str = ""

class DatabaseManager:
    """Gestiona la base de datos CSV de metadatos."""
    
    def __init__(self, config):
        self.config = config
        self._init_database()
    
    def _init_database(self):
        """Inicializa el archivo CSV si no existe."""
        if not self.config.database_file.exists():
            with open(self.config.database_file, 'w') as f:
                header = ",".join(self.config.metadata_fields) + "\n"
                f.write(header)
    
    def add_record(self, file_info: FileMetadata):
        """Añade un nuevo registro a la base de datos."""
        # Convertir el dataclass a dict y luego a lista ordenada según metadata_fields
        info_dict = asdict(file_info)
        # Convertir Path a str
        info_dict['ruta'] = str(info_dict['ruta'])
        ordered_values = [str(info_dict[field]) for field in self.config.metadata_fields]
        
        with open(self.config.database_file, 'a') as f:
            line = ",".join(ordered_values) + "\n"
            f.write(line)

class Logger:
    """Registra operaciones en un archivo de log."""
    
    def __init__(self, config):
        self.config = config
    
    def log_operation(self, operation: str, file_path: Path, status: str, details: str = ""):
        """Registra una operación en el log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp},{operation},{file_path},{status},{details}\n"
        
        with open(self.config.log_file, 'a') as f:
            f.write(log_entry)

#################################################################################################################
# Procesamiento principal con paralelismo
class FileProcessor:
    """Orquesta el procesamiento de archivos con soporte para paralelismo."""
    
    def __init__(self):
        self.config = Config()
        self.classifier = FileClassifier(self.config)
        self.hash_manager = HashManager()
        self.database = DatabaseManager(self.config)
        self.logger = Logger(self.config)
        self.dupes_finder = DupesFinder(self.config)
    
    def _process_single_file(self, file_path: Path, file_type: str):
        """Procesa un solo archivo con reintentos y manejo de errores."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Paso 1: Calcular hash
                file_hash = self.hash_manager.calculate_blake3(file_path)
                
                # Paso 2: Preparar destino
                dest_dir = self.config.staging_dir / file_type
                dest_path = dest_dir / f"{file_hash}_{file_path.name}"
                
                # Paso 3: Verificar colisión de hash
                if not dest_path.exists():
                    # Mover el archivo (con operación atómica)
                    shutil.move(str(file_path), str(dest_path))
                    
                    # Paso 4: Recoger metadatos
                    file_stats = dest_path.stat()
                    metadata = FileMetadata(
                        ruta=dest_path,
                        nombre=dest_path.name,
                        tipo=file_type,
                        tamano_bytes=file_stats.st_size,
                        fecha_mod=datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                        hash_blake3=file_hash
                    )
                    
                    # Paso 5: Añadir a base de datos
                    self.database.add_record(metadata)
                    
                    # Paso 6: Loggear éxito
                    self.logger.log_operation(
                        "MOVE_FILE", file_path, "SUCCESS", 
                        f"Moved to {dest_path} (attempt {attempt+1})"
                    )
                else:
                    self.logger.log_operation(
                        "SKIP_FILE", file_path, "DUPLICATE", 
                        f"Hash collision detected (attempt {attempt+1})"
                    )
                return  # Salir después de éxito
            except OSError as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    self.logger.log_operation(
                        "PROCESS_FILE", file_path, "ERROR", 
                        f"Failed after {max_retries} attempts: {str(e)}"
                    )
            except Exception as e:
                self.logger.log_operation(
                    "PROCESS_FILE", file_path, "ERROR", 
                    f"Unhandled error: {str(e)} (attempt {attempt+1})"
                )
                return  # No reintentar para otros errores
    
    def process_files(self):
        """Procesa todos los archivos en paralelo."""
        classified_files = self.classifier.classify_files()
        
        # Configurar pool de procesos (usar 75% de los cores)
        num_workers = max(1, int(cpu_count() * 0.75))
        with Pool(processes=num_workers) as pool:
            # Usar starmap para pasar múltiples argumentos
            pool.starmap(self._process_single_file, classified_files)
        
        # Buscar duplicados exactos después de procesar todo
        self.dupes_finder.handle_duplicates(self.config.staging_dir, keep_in='staging')
        self.dupes_finder.handle_duplicates(self.config.raw_dir, keep_in='raw')

#################################################################################################################
# Función principal
def main():
    print("Iniciando procesamiento de archivos...")
    processor = FileProcessor()
    processor.process_files()
    print("Procesamiento completado. Revisa los logs para detalles.")

if __name__ == "__main__":
    main()