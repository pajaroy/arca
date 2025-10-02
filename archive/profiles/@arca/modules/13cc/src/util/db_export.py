# Script Simple para Exportar Todas las Tablas a CSV

"""
Script para exportar TODAS las tablas de una base de datos SQLite a archivos CSV

Estructura esperada del proyecto:
.
├── database/
│   └── 13cc.db          # Base de datos SQLite
└── archive/
    └── exports/         # Directorio donde se guardarán los CSVs
"""

import sqlite3
import csv
from pathlib import Path
from datetime import datetime

# 1. Configuración de rutas
# -------------------------
# Ruta a la base de datos (ajustar según tu estructura)
db_path = Path(__file__).parent.parent.parent / "database" / "13cc.db"

# Directorio de salida para los CSVs (se creará si no existe)
output_dir = Path(__file__).parent.parent.parent / "archive" / "exports"
output_dir.mkdir(parents=True, exist_ok=True)

# 2. Conectar a la base de datos
# -----------------------------
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 3. Obtener lista de todas las tablas
# -----------------------------------
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in cursor.fetchall()]

# 4. Exportar cada tabla a CSV
# ---------------------------
for table_name in tables:
    # Generar nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"{table_name}_{timestamp}.csv"
    csv_path = output_dir / csv_filename
    
    # Obtener datos de la tabla
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    # Escribir archivo CSV
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(column_names)  # Escribir encabezados
        writer.writerows(rows)        # Escribir datos
    
    print(f"Exportada tabla '{table_name}' a {csv_path}")

# 5. Cerrar conexión
# -----------------
conn.close()
print("Exportación completada")

"""
## Características:

1. **Automatización completa**: Exporta todas las tablas sin necesidad de especificarlas
2. **Manejo de rutas**: Usa `pathlib` para compatibilidad entre sistemas
3. **Organización de archivos**:
   - Cada CSV lleva el nombre de la tabla + timestamp
   - Se guardan en el directorio `archive/exports`
4. **Estructura clara**: Cada paso está comentado
5. **Robustez básica**:
   - Crea el directorio de salida si no existe
   - Cierra siempre la conexión a la BD

## Uso:

Simplemente ejecuta el script y exportará todas las tablas automáticamente:

```bash
python3 src/util/db_export.py
```
"""