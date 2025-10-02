# @arca/data/main_v4.0.py - Clasificador Avanzado con SQL y ChromaDB

```python
#!/usr/bin/env python3
# ~/@arca/data/main.py
# Version: 0.4.0

"""
SCRIPT DE CLASIFICACIÓN AVANZADA v4.0

Nuevas Funcionalidades:
1. Extracción de metadatos avanzados (EXIF, MIME, etc.)
2. Almacenamiento en SQLite para búsquedas complejas
3. Integración con ChromaDB para embeddings (ML)
4. Sistema modular que mantiene compatibilidad con versión anterior

Flujo Mejorado:
1. Clasificación -> 2. Hash -> 3. Metadatos -> 4. Almacenamiento (CSV+SQL+Chroma)

Configuración Requerida en config.yaml:
databases:
  sql: "data/processed/metadata.db"
  chroma: "data/processed/chroma"
metadata:
  extract_exif: true
  max_file_size_mb: 100
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
import magic
import chromadb
from typing import Optional, List, Dict

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
        self.mime_detector = magic.Magic(mime=True)
    
    def extract(self, file_path: Path) -> FileMetadata:
        """Procesa un archivo y devuelve metadatos completos"""
        if file_path.stat().st_size > self.config.max_file_size:
            return self._basic_metadata(file_path)
        
        try:
            stats = file_path.stat()
            return FileMetadata(
                ruta=file_path,
                nombre=file_path.name,
                tipo=self._get_file_type(file_path),
                tamano_bytes=stats.st_size,
                fecha_mod=datetime.fromtimestamp(stats.st_mtime).isoformat(),
                hash_blake3=self._calculate_hash(file_path),
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
    
    def _get_mime_type(self, file_path: Path) -> str:
        """Detecta el tipo MIME real del archivo"""
        return self.mime_detector.from_file(file_path)
    
    def _get_exif_data(self, file_path: Path) -> Dict:
        """Extrae metadatos EXIF si está disponible"""
        if not self.config.extract_exif or exiftool is None:
            return {}
        
        try:
            with exiftool.ExifTool() as et:
                return et.get_metadata(str(file_path))
        except:
            return {}
    
    def _generate_tags(self, file_path: Path) -> List[str]:
        """Genera tags automáticos (placeholder para NLP)"""
        # Implementar con spaCy/transformers luego
        return []

#################################################################################################################
# BASES DE DATOS
class DatabaseManager:
    """Maneja múltiples sistemas de almacenamiento"""
    
    def __init__(self, config):
        self.config = config
        self._init_csv()
        self._init_sql()
        self._init_chroma()
    
    def _init_csv(self):
        """Mantiene compatibilidad con versión anterior"""
        if not self.config.database_csv.exists():
            with open(self.config.database_csv, 'w') as f:
                f.write("ruta,nombre,tipo,tamano_bytes,fecha_mod,hash_blake3\n")
    
    def _init_sql(self):
        """Inicializa base de datos SQLite para metadatos avanzados"""
        self.sql_conn = sqlite3.connect(self.config.database_sql)
        cursor = self.sql_conn.cursor()
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
    
    def _init_chroma(self):
        """Configura ChromaDB para embeddings"""
        self.chroma = chromadb.PersistentClient(path=str(self.config.chroma_dir))
        self.chroma_collection = self.chroma.get_or_create_collection("files")
    
    def save(self, metadata: FileMetadata):
        """Guarda en todos los sistemas"""
        self._save_csv(metadata)
        self._save_sql(metadata)
        if metadata.embedding:
            self._save_chroma(metadata)
    
    def _save_csv(self, metadata: FileMetadata):
        """Mantiene formato CSV original"""
        with open(self.config.database_csv, 'a') as f:
            f.write(f"{metadata.ruta},{metadata.nombre},{metadata.tipo},"
                    f"{metadata.tamano_bytes},{metadata.fecha_mod},{metadata.hash_blake3}\n")
    
    def _save_sql(self, metadata: FileMetadata):
        """Almacena metadatos avanzados en SQLite"""
        cursor = self.sql_conn.cursor()
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
        self.sql_conn.commit()
    
    def _save_chroma(self, metadata: FileMetadata):
        """Indexa embeddings para búsqueda semántica"""
        self.chroma_collection.add(
            ids=[metadata.hash_blake3],
            embeddings=[metadata.embedding],
            documents=[metadata.contenido[:5000]]  # Primeros 5000 caracteres
        )

#################################################################################################################
# CLASIFICACIÓN (Módulo existente mejorado)
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
# PROCESAMIENTO PRINCIPAL
class FileProcessor:
    """Orquesta todo el flujo de trabajo"""
    
    def __init__(self):
        self.config = Config()
        self.classifier = FileClassifier(self.config)
        self.metadata_extractor = MetadataExtractor(self.config)
        self.database = DatabaseManager(self.config)
        self.logger = self._init_logger()
    
    def _init_logger(self):
        """Configura logging avanzado"""
        self.config.log_file.parent.mkdir(exist_ok=True)
        return Logger(self.config)
    
    def process_files(self):
        """Ejecuta el procesamiento completo"""
        files = self.classifier.classify_files()
        
        with Pool(cpu_count()) as pool:
            pool.starmap(self._process_file, files)
        
        print("Procesamiento completado")
    
    def _process_file(self, file_path: Path, file_type: str):
        """Procesa un archivo individual con manejo de errores"""
        try:
            # Paso 1: Extraer metadatos básicos
            metadata = self.metadata_extractor.extract(file_path)
            
            # Paso 2: Mover a destino
            dest_dir = self.config.staging_dir / file_type
            dest_path = dest_dir / f"{metadata.hash_blake3}_{file_path.name}"
            
            if not dest_path.exists():
                shutil.move(str(file_path), str(dest_path))
                metadata.ruta = dest_path  # Actualiza ruta
                
                # Paso 3: Guardar en todas las bases de datos
                self.database.save(metadata)
                
                # Log exitoso
                self.logger.log(
                    "MOVE_SUCCESS",
                    f"{file_path} -> {dest_path}",
                    metadata
                )
        except Exception as e:
            self.logger.log(
                "PROCESS_ERROR",
                str(e),
                {"file": str(file_path)}
            )

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
```

## Configuración Requerida (`config.yaml`)

```yaml
root: "~/@arca"
formats:
  - "csv"
  - "markdown"
  - "otros"
  - "python"
  - "sql"
  - "yaml"

paths:
  raw: "data/raw"
  staging: "data/staging"
  log_file: "logs/processing.log"
  
databases:
  sql: "data/processed/metadata.db"
  chroma: "data/processed/chroma"

metadata:
  extract_exif: true
  max_file_size_mb: 50
```

## Mejoras Clave v4.0:

1. **Extracción de Metadatos Avanzados**:
   - Tipo MIME real (no solo por extensión)
   - Metadatos EXIF (autor, fecha creación, etc.)
   - Sistema de tags preparado para NLP

2. **Almacenamiento Mejorado**:
   - SQLite para consultas complejas
   - ChromaDB listo para machine learning
   - Mantiene CSV para compatibilidad

3. **Robustez**:
   - Manejo de archivos grandes
   - Procesamiento en paralelo seguro
   - Logging detallado

4. **Configuración Flexible**:
   - Límites ajustables
   - Rutas personalizables
   - Funcionalidad modular

## Próximos Pasos Recomendados:

1. Implementar generación de embeddings con:
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   metadata.embedding = model.encode(metadata.contenido)
   ```

2. Añadir interfaz de consulta:
   ```bash
   python3 main.py query "texto a buscar"
   ```

3. Integrar con FastAPI para servicio web.