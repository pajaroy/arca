# Script de Restauración de Base de Datos (db_restore.py)

"""
Script para restaurar la base de datos desde el último backup disponible

Estructura esperada:
.
├── archive/
│   └── backup/          # Directorio con backups (formato: 13cc_backup_YYYYMMDD_HHMMSS.db.gz)
└── database/
    └── 13cc.db          # Base de datos actual que será reemplazada
"""

import gzip
import os
from pathlib import Path
from datetime import datetime

def get_latest_backup(backup_dir):
    """
    Encuentra el archivo de backup más reciente en el directorio especificado
    
    Args:
        backup_dir (Path): Directorio donde buscar los backups
        
    Returns:
        Path: Ruta al backup más reciente
    Raises:
        FileNotFoundError: Si no hay backups disponibles
    """
    backups = list(backup_dir.glob('13cc_backup_*.db.gz'))
    
    if not backups:
        raise FileNotFoundError("No se encontraron archivos de backup")
    
    # Ordenar por fecha (el nombre contiene timestamp)
    backups.sort(reverse=True)
    return backups[0]

def restore_database(backup_file, target_db):
    """
    Restaura un backup comprimido a la base de datos destino
    
    Args:
        backup_file (Path): Ruta al archivo de backup (.gz)
        target_db (Path): Ruta donde se restaurará la base de datos
    """
    # Eliminar la base de datos actual si existe
    if target_db.exists():
        target_db.unlink()
    
    # Descomprimir y restaurar el backup
    with gzip.open(backup_file, 'rb') as f_in:
        with open(target_db, 'wb') as f_out:
            f_out.write(f_in.read())

def log_restoration(backup_file, log_file):
    """
    Registra la operación de restauración en el log
    
    Args:
        backup_file (Path): Archivo de backup usado
        log_file (Path): Archivo de log
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(log_file, 'a') as log:
        log.write(f"{timestamp} - Restauración desde: {backup_file.name}\n")

def main():
    # 1. Configurar rutas
    project_root = Path(__file__).parents[2]
    backup_dir = project_root / "archive" / "backup"
    target_db = project_root / "database" / "13cc.db"
    log_file = backup_dir / "backup.log"
    
    try:
        # 2. Encontrar el backup más reciente
        latest_backup = get_latest_backup(backup_dir)
        print(f"Restaurando desde: {latest_backup.name}")
        
        # 3. Realizar la restauración
        restore_database(latest_backup, target_db)
        
        # 4. Registrar en el log
        log_restoration(latest_backup, log_file)
        
        print("Restauración completada exitosamente")
        
    except Exception as e:
        print(f"Error durante la restauración: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()

"""
## Características del Script:

1. **Búsqueda automática del último backup**:
   - Analiza los nombres de archivo con patrón `13cc_backup_YYYYMMDD_HHMMSS.db.gz`
   - Selecciona el más reciente por timestamp

2. **Proceso de restauración seguro**:
   - Elimina la base de datos existente antes de restaurar
   - Maneja correctamente la descompresión GZIP

3. **Registro de operaciones**:
   - Añade una entrada al archivo `backup.log` con la restauración realizada

4. **Manejo de errores**:
   - Detecta cuando no hay backups disponibles
   - Captura otros errores potenciales durante el proceso

5. **Estructura clara**:
   - Funciones separadas para cada tarea específica
   - Comentarios explicativos en cada sección

## Uso:

Simplemente ejecutar el script desde la terminal:

```bash
python3 src/util/db_restore.py
```

El script:
1. Buscará automáticamente el backup más reciente
2. Reemplazará la base de datos actual (`database/13cc.db`)
3. Registrará la operación en el log

## Notas de Seguridad:

- El script **sobrescribe** la base de datos actual sin confirmación
- Recomiendo siempre:
  - Hacer un nuevo backup antes de restaurar
  - Verificar que el backup seleccionado es el correcto
  - Tener cuidado al ejecutarlo en producción
"""