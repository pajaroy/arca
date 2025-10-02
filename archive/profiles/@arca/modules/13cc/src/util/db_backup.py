import os
import sqlite3
import gzip
from datetime import datetime
from pathlib import Path

def backup_database(db_path, backup_dir):
    """
    Realiza backup comprimido de la base de datos SQLite
    
    Args:
        db_path (str): Ruta al archivo de base de datos
        backup_dir (str): Directorio donde guardar el backup
        
    Returns:
        str: Ruta del archivo de backup creado
    """
    # Crear directorio de backup si no existe
    Path(backup_dir).mkdir(parents=True, exist_ok=True)
    
    # Generar nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_name = Path(db_path).stem
    backup_name = f"{db_name}_backup_{timestamp}.db.gz"
    backup_path = Path(backup_dir) / backup_name
    
    # Leer y comprimir la base de datos
    with open(db_path, 'rb') as f_in:
        with gzip.open(backup_path, 'wb') as f_out:
            f_out.writelines(f_in)
    
    # Registrar en log
    log_path = Path(backup_dir) / "backup.log"
    with open(log_path, 'a') as log:
        log.write(f"{timestamp} - Backup creado: {backup_name}\n")
    
    return str(backup_path)

if __name__ == "__main__":
    # Ejemplo de uso directo
    project_root = Path(__file__).parents[2]
    db_path = project_root / "database" / "13cc.db"
    backup_dir = project_root / "archive" / "backup"
    
    backup_file = backup_database(db_path, backup_dir)
    print(f"Backup creado en: {backup_file}")