#!/usr/bin/env python3
# ~/@arca/source/main.py
# Version: 0.2.0
# Descripcion: Script para clasificar archivos por formato
#  - Extrae archivos de cualquier carpeta
#  - Calcula el hash con blake2b (similar a blake3)
#  - Verifica los hash en destino para evitar colisiones
#  - Prepara base para implementar fdupes (duplicados textuales)
#  - Genera logs de cada operación
# Flujo de trabajo:
#  - Toma los archivos desde /data/raw
#  - Los clasifica por formato
#  - Calcula el hash con blake2b 
#  - Deposita los archivos en /data/staging
#  - Inicia la base de datos csv
#  - indexa todo en /data/staging/database.csv
#  
# Reglas de oro:
#  - Todo debe poder ser exportado para luego ir extendiendolo para cargar todo a sql.
# 
# Estructura del script:
#  - Config: Carga la configuración base 
#  - FileClassifier: Clasifica archivos por formato
#  - HashManager: Maneja cálculos y verificación de hashes
#  - DatabaseManager: Gestiona la base de datos CSV
#  - Logger: Registra todas las operaciones
#  - FileProcessor: Orquesta el proceso completo
#################################################################################################################

import os
import hashlib
import shutil
from datetime import datetime
import yaml
from pathlib import Path

#################################################################################################################
# Configuración base del sistema
# Esto podríamos moverlo luego a un config.yaml
class Config:
    """Clase que maneja todas las configuraciones del sistema.
    
    Define las rutas base, formatos de archivo permitidos y estructura de directorios.
    Crea los directorios necesarios al inicializarse.
    """
    def __init__(self):
        # Directorio raíz del proyecto
        self.root = os.path.expanduser("~/@arca")
        
        # Formatos de archivo que reconoceremos
        self.formats = ["csv", "markdown", "otros", "python", "sql", "yaml"]
        
        # Campos que tendrá nuestra base de datos/metadata
        self.metadata_fields = [
            "ruta", "nombre", "tipo", "tamano_bytes", 
            "fecha_mod", "hash_blake3", "contenido"
        ]
        
        # Rutas importantes
        self.raw_dir = os.path.join(self.root, "data/raw")          # Donde se colocan archivos nuevos
        self.staging_dir = os.path.join(self.root, "data/staging")  # Donde se clasifican
        self.log_file = os.path.join(self.root, "datalogs/datalogs.csv")  # Registro de operaciones
        self.database_file = os.path.join(self.root, "data/staging/database.csv")  # Base de datos
        
        # Aseguramos que existan todos los directorios necesarios
        self._create_directories()
    
    def _create_directories(self):
        """Crea todos los directorios necesarios si no existen."""
        # Directorios principales
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.staging_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Directorios para cada tipo de archivo
        for format_dir in self.formats:
            os.makedirs(os.path.join(self.staging_dir, format_dir), exist_ok=True)

#################################################################################################################
# Clasificador de archivos
class FileClassifier:
    """Clase responsable de clasificar archivos por su tipo/extensión."""
    
    def __init__(self, config):
        self.config = config
    
    def get_file_type(self, file_path):
        """Determina el tipo de archivo basado en su extensión.
        
        Args:
            file_path (str): Ruta completa al archivo
            
        Returns:
            str: Tipo de archivo según self.config.formats
        """
        # Extraemos la extensión del archivo (sin el punto)
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        
        # Asignamos a categorías conocidas
        if ext in self.config.formats:
            return ext
        elif ext in ['txt', 'md', 'markdown']:
            return 'markdown'
        elif ext in ['py']:
            return 'python'
        else:
            return 'otros'
    
    def classify_files(self):
        """Clasifica todos los archivos en la carpeta raw.
        
        Returns:
            list: Lista de tuplas (ruta_archivo, tipo_archivo)
        """
        classified_files = []
        
        # Recorremos recursivamente la carpeta raw
        for root_dir, _, files in os.walk(self.config.raw_dir):
            for file in files:
                file_path = os.path.join(root_dir, file)
                file_type = self.get_file_type(file_path)
                classified_files.append((file_path, file_type))
        
        return classified_files

#################################################################################################################
# Manejo de Hash
class HashManager:
    """Clase que maneja todo lo relacionado con hashes de archivos."""
    
    @staticmethod
    def calculate_blake3(file_path):
        """Calcula el hash Blake2b (similar a Blake3) de un archivo.
        
        Args:
            file_path (str): Ruta al archivo a hashear
            
        Returns:
            str: Hash hexadecimal del archivo
        """
        hasher = hashlib.blake2b()
        
        # Leemos el archivo en chunks para no consumir mucha memoria
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):  # Lee en bloques de 8KB
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    def check_hash_collision(self, target_dir, hash_value):
        """Verifica si ya existe un archivo con el mismo hash en el directorio destino.
        
        Args:
            target_dir (str): Directorio donde buscar colisiones
            hash_value (str): Hash a verificar
            
        Returns:
            bool: True si hay colisión, False si no
        """
        for root_dir, _, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root_dir, file)
                if self.calculate_blake3(file_path) == hash_value:
                    return True
        return False

#################################################################################################################

class FdupesManager:
    """Clase para manejar la detección de duplicados exactos usando fdupes.
    
    Debe ejecutarse después del hashing para verificar duplicados exactos,
    incluso si tienen nombres diferentes.
    """
    
    def __init__(self, config):
        self.config = config
    
    def find_duplicates(self, directory):
        """Encuentra archivos duplicados en un directorio usando fdupes.
        
        Args:
            directory (str): Ruta al directorio a escanear
            
        Returns:
            list: Lista de listas, donde cada sublista contiene rutas de archivos idénticos
        """
        try:
            # Ejecutamos fdupes y capturamos la salida
            result = subprocess.run(
                ['fdupes', '-r', directory],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Procesamos la salida: grupos de archivos separados por líneas vacías
            groups = []
            current_group = []
            
            for line in result.stdout.split('\n'):
                if line.strip():  # Si la línea no está vacía
                    current_group.append(line.strip())
                elif current_group:  # Línea vacía y tenemos un grupo
                    groups.append(current_group)
                    current_group = []
            
            return groups
            
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar fdupes: {e}")
            return []
    
    def handle_duplicates(self, directory, keep_in='staging'):
        """Maneja los archivos duplicados, conservando solo una copia.
        
        Args:
            directory (str): Directorio a analizar
            keep_in (str): Dónde conservar el original ('staging' o 'raw')
        """
        duplicate_groups = self.find_duplicates(directory)
        
        for group in duplicate_groups:
            if len(group) > 1:  # Si hay duplicados reales
                # Conservamos el primero del grupo
                original = group[0]
                
                # Los demás son duplicados a manejar
                for duplicate in group[1:]:
                    if keep_in == 'staging' and duplicate.startswith(self.config.raw_dir):
                        os.remove(duplicate)
                    elif keep_in == 'raw' and duplicate.startswith(self.config.staging_dir):
                        os.remove(duplicate)
                    else:
                        # Caso especial: duplicados entre diferentes lugares
                        # Por defecto conservamos el que está en staging
                        if duplicate.startswith(self.config.raw_dir):
                            os.remove(duplicate)

#################################################################################################################
# Database y Logging

class DatabaseManager:
    """Clase que maneja la base de datos CSV de archivos indexados."""
    
    def __init__(self, config):
        self.config = config
        self._init_database()
    
    def _init_database(self):
        """Inicializa el archivo CSV de la base de datos si no existe."""
        if not os.path.exists(self.config.database_file):
            with open(self.config.database_file, 'w') as f:
                header = ",".join(self.config.metadata_fields) + "\n"
                f.write(header)
    
    def add_record(self, file_info):
        """Añade un nuevo registro a la base de datos.
        
        Args:
            file_info (dict): Diccionario con los campos definidos en config.metadata_fields
        """
        with open(self.config.database_file, 'a') as f:
            line = ",".join(str(value) for value in file_info.values()) + "\n"
            f.write(line)

class Logger:
    """Clase que maneja el registro de operaciones del sistema."""
    
    def __init__(self, config):
        self.config = config
    
    def log_operation(self, operation, file_path, status, details=""):
        """Registra una operación en el archivo de log.
        
        Args:
            operation (str): Tipo de operación (ej. "MOVE_FILE")
            file_path (str): Ruta del archivo afectado
            status (str): Resultado ("SUCCESS", "ERROR", etc.)
            details (str): Información adicional (opcional)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp},{operation},{file_path},{status},{details}\n"
        
        with open(self.config.log_file, 'a') as f:
            f.write(log_entry)

#################################################################################################################
# Procesamiento principal
class FileProcessor:
    """Clase principal que orquesta todo el proceso de clasificación."""
    
    def __init__(self):
        # Inicializamos todos los componentes
        self.config = Config()
        self.classifier = FileClassifier(self.config)
        self.hash_manager = HashManager()
        self.database = DatabaseManager(self.config)
        self.logger = Logger(self.config)
        self.fdupes = FdupesManager(self.config)
    
    def process_files(self):
        """Procesa todos los archivos en la carpeta raw."""
        # Obtenemos la lista de archivos clasificados
        classified_files = self.classifier.classify_files()
        
        # Procesamos cada archivo
        for file_path, file_type in classified_files:
            try:
                # Paso 1: Calcular hash del archivo
                file_hash = self.hash_manager.calculate_blake3(file_path)
                
                # Paso 2: Determinar directorio destino según tipo
                dest_dir = os.path.join(self.config.staging_dir, file_type)
                # Nombre final: hash_nombreoriginal
                dest_path = os.path.join(dest_dir, f"{file_hash}_{os.path.basename(file_path)}")
                
                # Paso 3: Verificar si ya existe un archivo con este hash
                if not self.hash_manager.check_hash_collision(dest_dir, file_hash):
                    # Paso 4: Mover el archivo a su nueva ubicación
                    shutil.move(file_path, dest_path)
                    
                    # Paso 5: Recoger metadatos del archivo
                    file_stats = os.stat(dest_path)
                    metadata = {
                        "ruta": dest_path,
                        "nombre": os.path.basename(dest_path),
                        "tipo": file_type,
                        "tamano_bytes": file_stats.st_size,
                        "fecha_mod": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                        "hash_blake3": file_hash,
                        "contenido": ""  # Podemos implementar extracción de contenido después
                    }
                    
                    # Paso 6: Añadir a la base de datos
                    self.database.add_record(metadata)
                    
                    # Paso 7: Registrar operación exitosa
                    self.logger.log_operation(
                        "MOVE_FILE", file_path, "SUCCESS", 
                        f"Moved to {dest_path}"
                    )
                else:
                    # Archivo duplicado (mismo hash)
                    self.logger.log_operation(
                        "SKIP_FILE", file_path, "DUPLICATE", 
                        "Hash collision detected"
                    )
            except Exception as e:
                # Registrar cualquier error ocurrido
                self.logger.log_operation(
                    "PROCESS_FILE", file_path, "ERROR", 
                    str(e)
                )
                print("Buscando duplicados exactos...")
                self.fdupes.handle_duplicates(self.config.staging_dir, keep_in='staging')

#################################################################################################################
# Función principal
def main():
    """Función principal que inicia el procesamiento."""
    print("Iniciando procesamiento de archivos...")
    processor = FileProcessor()
    processor.process_files()
    print("Procesamiento completado. Revisa los logs para detalles.")

if __name__ == "__main__":
    main()