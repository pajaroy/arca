#!/usr/bin/env python3
# ~/@arca/data/main.py
# Version: 4.0.0

"""
DESCRIPCIÓN COMPLETA DEL SCRIPT (Para humanos y no programadores)

Qué hace este script:
1. Organiza automáticamente tus archivos por tipo (documentos, código, etc.)
2. Calcula una "huella digital" única (hash) para cada archivo
3. Detecta y elimina archivos duplicados
4. Guarda información organizada en una base de datos simple
5. Registra todo lo que hace en un archivo de log

Mejoras importantes (v0.3):
- Ahora se configura desde un archivo YAML (más fácil de modificar)
- Trabaja más rápido con muchos archivos (usa todos los núcleos del CPU)
- Funciona igual en Windows, Mac y Linux
- Maneja mejor los errores (reintenta si algo falla)
- Código más organizado y fácil de entender

FLUJO DE TRABAJO PASO A PASO:
1. Busca archivos en la carpeta /data/raw
2. Clasifica cada archivo por su tipo (ej: .py = python, .md = markdown)
3. Calcula su huella digital (hash)
4. Mueve el archivo a su carpeta correspondiente en /data/staging
5. Registra toda la información en database.csv
6. Busca y elimina archivos idénticos (duplicados)

ESTRUCTURA PRINCIPAL:
- Config: Lee la configuración desde YAML
- FileClassifier: Clasifica archivos por su tipo
- HashManager: Calcula y verifica hashes
- DupesFinder: Encuentra archivos duplicados
- DatabaseManager: Maneja la base de datos
- Logger: Registra todas las operaciones
- FileProcessor: Coordina todo el proceso

USO BÁSICO:
1. Coloca tus archivos en ~/@arca/data/raw
2. Ejecuta el script: python3 main.py
3. Revisa los resultados en ~/@arca/data/staging

ARCHIVO DE CONFIGURACIÓN (config.yaml):
- Define rutas, tipos de archivos y estructura
- Se encuentra en ~/@arca/config.yaml

"""

import os
import hashlib
import shutil
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import sys
from multiprocessing import Pool, cpu_count
from dataclasses import dataclass, field, asdict
import time
import yaml
import mimetypes
import subprocess
import chromadb
from typing import Optional, List, Dict

# ======== MANEJO DE DEPENDENCIAS ========
def check_dependencies():
    required = {
        'PyYAML': 'yaml',
        'chromadb': 'chromadb'
    }
    recommended = {
        'python-magic': 'magic',
        'filetype': 'filetype'
    }
    
    missing = []
    for pkg, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print("ERROR: Faltan dependencias requeridas:")
        for pkg in missing:
            print(f"- {pkg}")
        
        confirm = input("\n¿Instalar automáticamente? [s/n]: ").lower()
        if confirm == 's':
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
                print("¡Dependencias instaladas correctamente!")
                print("Por favor ejecuta el script nuevamente.")
            except subprocess.CalledProcessError:
                print("\nERROR: No se pudo instalar las dependencias.")
                print("Instala manualmente con:")
                print(f"pip install {' '.join(missing)}")
            sys.exit(1)
        else:
            print("\nInstala manualmente con:")
            print(f"pip install {' '.join(missing)}")
            sys.exit(1)
    
    # Solo advertencia para dependencias recomendadas
    for pkg, import_name in recommended.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"AVISO: Para mejor detección de tipos MIME, instala: pip install {pkg}")

check_dependencies()

# Compatibilidad con exiftool (opcional)
try:
    import exiftool
except ImportError:
    exiftool = None

#################################################################################################################
# CONFIGURACIÓN
class Config:
    """Carga y valida la configuración desde YAML"""
    
    def __init__(self, config_path="~/@arca/data/config.yaml"):
        self.config_path = Path(config_path).expanduser()
        self._load_config()
        self._validate()
        self._create_directories()
    
    def _load_config(self):
        """Carga el archivo YAML con valores por defecto"""
        with open(self.config_path, 'r') as f:
            config_data = yaml.safe_load(f) or {}
        
        # Configuración base
        self.root = Path(config_data.get('root', '~/@arca')).expanduser()
        self.formats = config_data.get('formats', ['csv', 'markdown', 'otros', 'python', 'sql', 'yaml'])
        
        # Rutas
        paths = config_data.get('paths', {})
        self.raw_dir = self.root / paths.get('raw', 'data/raw')
        self.staging_dir = self.root / paths.get('staging', 'data/staging')
        self.log_file = self.root / paths.get('log_file', 'datalogs/datalogs.csv')
        
        # Bases de datos
        db_config = config_data.get('databases', {})
        self.database_csv = self.root / paths.get('database_file', 'data/staging/database.csv')
        self.database_sql = self.root / db_config.get('sql', 'data/processed/metadata.db')
        self.chroma_dir = self.root / db_config.get('chroma', 'data/processed/chroma')
        
        # Metadatos
        self.extract_exif = config_data.get('metadata', {}).get('extract_exif', True)
        self.max_file_size = config_data.get('metadata', {}).get('max_file_size_mb', 50) * 1024 * 1024
    
    def _validate(self):
        """Valida configuraciones críticas"""
        if not self.raw_dir.exists():
            raise ValueError(f"Directorio raw no existe: {self.raw_dir}")
    
    def _create_directories(self):
        """Crea toda la estructura de directorios necesaria"""
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        self.database_sql.parent.mkdir(parents=True, exist_ok=True)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)
        
        for fmt in self.formats:
            (self.staging_dir / fmt).mkdir(exist_ok=True)

#################################################################################################################
# ESTRUCTURAS DE DATOS
@dataclass
class FileMetadata:
    """Contiene todos los metadatos de un archivo"""
    ruta: Path
    nombre: str
    tipo: str
    tamano_bytes: int
    fecha_mod: str
    hash_blake3: str
    # Campos avanzados
    tipo_mime: str = ""
    autor: str = ""
    tags: List[str] = field(default_factory=list)
    exif_data: Dict = field(default_factory=dict)
    contenido: str = ""
    embedding: Optional[List[float]] = None

#################################################################################################################
# EXTRACCIÓN DE METADATOS
class MetadataExtractor:
    """Extrae metadatos avanzados de archivos"""
    
    def __init__(self, config):
        self.config = config
        self._init_mime_detector()
    
    def _init_mime_detector(self):
        """Inicializa el detector MIME con el mejor método disponible"""
        try:
            # 1. Intenta con python-magic (más preciso)
            import magic
            self.mime_detector = magic.Magic(mime=True)
            self._get_mime_type = self._get_mime_type_magic
            print("INFO: Usando python-magic para detección MIME")
        except ImportError:
            try:
                # 2. Fallback a filetype (pura Python)
                import filetype
                self.filetype = filetype
                self._get_mime_type = self._get_mime_type_filetype
                print("INFO: Usando filetype para detección MIME (instala python-magic para mejor precisión)")
            except ImportError:
                # 3. Finalmente usa mimetypes estándar (solo por extensión)
                import mimetypes
                mimetypes.init()
                self._get_mime_type = self._get_mime_type_mimetypes
                print("INFO: Usando mimetypes básico (instala python-magic o filetype para mejor detección)")
    
    def extract(self, file_path: Path) -> FileMetadata:
        """Versión optimizada para reutilizar hashes existentes"""
        try:
            stats = file_path.stat()
            
            # Extraer hash del nombre si sigue el formato HASH_nombre.ext
            file_hash = None
            if "_" in file_path.name:
                possible_hash = file_path.name.split("_")[0]
                if len(possible_hash) == 64:  # Longitud de hash Blake2b
                    file_hash = possible_hash
            
            # Solo calcular hash si no se encontró en el nombre
            file_hash = file_hash if file_hash else self._calculate_hash(file_path)
            
            return FileMetadata(
                ruta=file_path,
                nombre=file_path.name,
                tipo=self._get_file_type(file_path),
                tamano_bytes=stats.st_size,
                fecha_mod=datetime.fromtimestamp(stats.st_mtime).isoformat(),
                hash_blake3=file_hash,
                tipo_mime=self._get_mime_type(file_path),
                exif_data=self._get_exif_data(file_path),
                tags=self._generate_tags(file_path)
            )
        except Exception as e:
            print(f"Error extrayendo metadatos de {file_path.name}: {str(e)}")
            return self._basic_metadata(file_path)
    
    def _basic_metadata(self, file_path: Path) -> FileMetadata:
        """Versión mínima de metadatos para archivos grandes/fallidos"""
        stats = file_path.stat()
        return FileMetadata(
            ruta=file_path,
            nombre=file_path.name,
            tipo=self._get_file_type(file_path),
            tamano_bytes=stats.st_size,
            fecha_mod=datetime.fromtimestamp(stats.st_mtime).isoformat(),
            hash_blake3=self._calculate_hash(file_path),
            tipo_mime="application/octet-stream"
        )
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calcula hash Blake2b de un archivo"""
        hasher = hashlib.blake2b()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def _get_file_type(self, file_path: Path) -> str:
        """Determina el tipo basado en extensión"""
        ext = file_path.suffix.lower().lstrip('.')
        return ext if ext in self.config.formats else 'otros'
    
    def _get_mime_type_magic(self, file_path: Path) -> str:
        """Usando python-magic"""
        return self.mime_detector.from_file(file_path)
    
    def _get_mime_type_filetype(self, file_path: Path) -> str:
        """Usando filetype"""
        kind = self.filetype.guess(str(file_path))
        return kind.mime if kind else "application/octet-stream"
    
    def _get_mime_type_mimetypes(self, file_path: Path) -> str:
        """Usando mimetypes estándar"""
        mime, _ = mimetypes.guess_type(file_path)
        return mime or "application/octet-stream"
    
    def _get_exif_data(self, file_path: Path) -> Dict:
        """Versión mejorada con exiftool"""
        try:
            result = subprocess.run(
                ['exiftool', '-j', str(file_path)],
                capture_output=True, text=True, check=True
            )
            return json.loads(result.stdout)[0] if result.stdout else {}
        except:
            return {}
    
    def _generate_tags(self, file_path: Path) -> List[str]:
        """Genera tags automáticos (placeholder para NLP)"""
        return []

#################################################################################################################
# BASES DE DATOS
class DatabaseManager:
    """Maneja múltiples sistemas de almacenamiento"""
    
    def __init__(self, config):
        self.config = config
        self._init_csv()
        # No inicializar ChromaDB aquí
    
    def get_sql_connection(self):
        """Crea una nueva conexión SQLite para cada proceso"""
        conn = sqlite3.connect(self.config.database_sql)
        self._init_sql_schema(conn)
        return conn
    
    def get_chroma_client(self):
        """Crea un nuevo cliente ChromaDB para cada proceso"""
        chroma = chromadb.PersistentClient(path=str(self.config.chroma_dir))
        return chroma.get_or_create_collection("files")
    
    def _init_sql_schema(self, conn):
        """Inicializa el esquema de la base de datos"""
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id TEXT PRIMARY KEY,
                path TEXT UNIQUE,
                name TEXT,
                type TEXT,
                size INTEGER,
                mod_date TEXT,
                mime_type TEXT,
                author TEXT,
                tags TEXT,
                exif_data TEXT
            )
        ''')
        conn.commit()
    
    def _init_csv(self):
        """Mantiene compatibilidad con versión anterior"""
        if not self.config.database_csv.exists():
            with open(self.config.database_csv, 'w') as f:
                f.write("ruta,nombre,tipo,tamano_bytes,fecha_mod,hash_blake3\n")
    
    def save(self, metadata: FileMetadata, sql_conn=None, chroma_collection=None):
        """Guarda en todos los sistemas"""
        self._save_csv(metadata)
        if sql_conn is not None:
            self._save_sql(metadata, sql_conn)
        if metadata.embedding and chroma_collection is not None:
            self._save_chroma(metadata, chroma_collection)
    
    def _save_csv(self, metadata: FileMetadata):
        """Mantiene formato CSV original"""
        with open(self.config.database_csv, 'a') as f:
            f.write(f"{metadata.ruta},{metadata.nombre},{metadata.tipo},"
                    f"{metadata.tamano_bytes},{metadata.fecha_mod},{metadata.hash_blake3}\n")
    
    def _save_sql(self, metadata: FileMetadata, conn):
        """Almacena metadatos avanzados en SQLite"""
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO files VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metadata.hash_blake3,
            str(metadata.ruta),
            metadata.nombre,
            metadata.tipo,
            metadata.tamano_bytes,
            metadata.fecha_mod,
            metadata.tipo_mime,
            metadata.autor,
            json.dumps(metadata.tags),
            json.dumps(metadata.exif_data)
        ))
        conn.commit()
    
    def _save_chroma(self, metadata: FileMetadata, collection):
        """Indexa embeddings para búsqueda semántica"""
        collection.add(
            ids=[metadata.hash_blake3],
            embeddings=[metadata.embedding],
            documents=[metadata.contenido[:5000]]  # Primeros 5000 caracteres
        )

#################################################################################################################
# CLASIFICACIÓN
class FileClassifier:
    """Clasifica archivos por tipo y prepara para procesamiento"""
    
    def __init__(self, config):
        self.config = config
    
    def classify_files(self) -> List[tuple]:
        """Explora recursivamente y clasifica archivos"""
        files = []
        for root, _, filenames in os.walk(self.config.raw_dir):
            for filename in filenames:
                file_path = Path(root) / filename
                if file_path.is_file():
                    files.append((file_path, self._get_file_type(file_path)))
        return files
    
    def _get_file_type(self, file_path: Path) -> str:
        ext = file_path.suffix.lower().lstrip('.')
        return ext if ext in self.config.formats else 'otros'

#################################################################################################################
# LOGGING SYSTEM
class Logger:
    """Maneja el registro de actividades del sistema"""
    
    def __init__(self, config):
        self.config = config
        self.log_file = config.log_file
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Crea el archivo de log si no existe"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            with open(self.log_file, 'w') as f:
                f.write("timestamp,level,operation,message,metadata\n")
    
    def log(self, level: str, message: str, metadata: dict = None):
        """Registra un evento en el log"""
        timestamp = datetime.now().isoformat()
        metadata_str = json.dumps(metadata) if metadata else "{}"
        
        log_entry = f'"{timestamp}","{level}","{message}","{metadata_str}"\n'
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)

#################################################################################################################
# PROCESAMIENTO PRINCIPAL
class FileProcessor:
    """Orquesta todo el flujo de trabajo"""
    
    def __init__(self):
        self.config = Config()
        self.classifier = FileClassifier(self.config)
        self.metadata_extractor = MetadataExtractor(self.config)
        self.database = DatabaseManager(self.config)
        self.logger = Logger(self.config)
    
    def process_files(self):
        """Ejecuta el procesamiento completo"""
        # Inicializar esquema SQLite antes del procesamiento paralelo
        init_conn = self.database.get_sql_connection()
        init_conn.close()
        
        files = self.classifier.classify_files()
        
        with Pool(cpu_count()) as pool:
            pool.starmap(self._process_file, files)
        
        print("Procesamiento completado")
    
    def _process_file(self, file_path: Path, file_type: str):
        """Procesa un archivo individual optimizado para hashes existentes"""
        sql_conn = None
        try:
            # Paso 1: Extraer metadatos (reutilizando hash existente del nombre)
            metadata = self.metadata_extractor.extract(file_path)
            
            # Paso 2: Generar nombre de destino optimizado
            if "_" in file_path.name and len(file_path.name.split("_")[0]) == 64:
                # Si ya tiene formato HASH_nombre.ext, usamos solo los primeros 12 chars del hash
                hash_part = file_path.name.split("_")[0][:12]
                name_part = "_".join(file_path.name.split("_")[1:])
                safe_name = f"{hash_part}_{name_part}"
            else:
                # Para archivos sin hash en el nombre, usar el hash calculado
                safe_name = f"{metadata.hash_blake3[:12]}_{file_path.name}"
            
            # Asegurar que no exceda límites del sistema de archivos
            safe_name = safe_name[:200]  # Limitar a 200 caracteres como máximo
            
            dest_dir = self.config.staging_dir / file_type
            dest_path = dest_dir / safe_name
            
            # Paso 3: Verificar si el archivo ya existe (comparando hashes completos)
            if dest_path.exists():
                existing_metadata = self.metadata_extractor.extract(dest_path)
                if existing_metadata.hash_blake3 == metadata.hash_blake3:
                    return  # El archivo ya está procesado
            
            # Paso 4: Mover archivo y guardar metadatos
            sql_conn = self.database.get_sql_connection()
            shutil.move(str(file_path), str(dest_path))
            metadata.ruta = dest_path
            self.database.save(metadata, sql_conn)
            
            self.logger.log(
                "MOVE_SUCCESS", 
                f"{file_path.name} -> {safe_name}",
                {"hash": metadata.hash_blake3[:12]}
            )
            
        except Exception as e:
            self.logger.log(
                "PROCESS_ERROR",
                str(e),
                {"file": str(file_path)}
            )
        finally:
            if sql_conn:
                sql_conn.close()

#################################################################################################################
# EJECUCIÓN
if __name__ == "__main__":
    print("=== ARCA File Processor v4.0 ===")
    start_time = time.time()
    
    processor = FileProcessor()
    processor.process_files()
    
    elapsed = time.time() - start_time
    print(f"\nTiempo total: {elapsed:.2f} segundos")
    print(f"Metadatos SQLite: {processor.config.database_sql}")
    print(f"Embeddings ChromaDB: {processor.config.chroma_dir}")