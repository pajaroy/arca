import sqlite3
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
import ruamel.yaml

class DatabaseManager:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self.db_path = Path(self.config['paths']['database'])
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_logging()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Cargar configuración desde YAML"""
        with open(config_path, 'r') as file:
            yaml = ruamel.yaml.YAML()
            return yaml.load(file)
    
    def _init_logging(self):
        """Inicializar logging"""
        logging.basicConfig(
            level=self.config['logging']['level'],
            format=self.config['logging']['format'],
            datefmt=self.config['logging']['date_format']
        )
        self.logger = logging.getLogger(__name__)
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtener conexión a la base de datos con WAL habilitado"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=self.config['database']['timeout'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_database(self):
        """Inicializar base de datos con esquema"""
        schema_path = Path(self.config['meta']['schema'])
        if not schema_path.exists():
            raise FileNotFoundError(f"Esquema no encontrado: {schema_path}")
        
        with self.get_connection() as conn:
            with open(schema_path, 'r') as file:
                schema_sql = file.read()
            conn.executescript(schema_sql)
            self.logger.info("Base de datos inicializada correctamente")
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Ejecutar query y retornar cursor"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor
    
    def fetchone(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Ejecutar query y retornar una fila"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchone()
    
    def fetchall(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Ejecutar query y retornar todas las filas"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
    
    def insert_and_get_id(self, query: str, params: tuple = ()) -> int:
        """Insertar y retornar el ID generado"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.lastrowid

# Instancia global para uso en otros módulos
db_manager = DatabaseManager()