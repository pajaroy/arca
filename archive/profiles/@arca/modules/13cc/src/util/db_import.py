"""
Script final de importación con:
- Manejo especial para tablas con ID autoincremental
- Corrección de errores de sintaxis
- Eliminación de columnas ID redundantes
"""

import csv
import sqlite3
from pathlib import Path

def create_database_from_schema(db_path, schema_path):
    """Crea la BD desde schema.sql si no existe"""
    if not db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            with open(schema_path, 'r') as schema_file:
                schema_sql = schema_file.read()
            conn.executescript(schema_sql)
            conn.close()
            print("Base de datos creada desde schema.sql")
        except Exception as e:
            print(f"Error creando BD: {str(e)}")
            raise

def get_csv_files(exports_dir):
    """Obtiene todos los archivos CSV válidos"""
    return [f for f in exports_dir.glob('*.csv') if f.stat().st_size > 0]

def get_table_name_from_csv(csv_file):
    """Extrae el nombre correcto de la tabla"""
    if 'sqlite_sequence' in csv_file.stem:
        return 'sqlite_sequence'
    return csv_file.stem.split('_')[0]

def should_skip_column(table_name, column_name):
    """Determina si una columna debe ser omitida (IDs redundantes)"""
    skip_rules = {
        'harvest': ['harvest_id'],
        'harvest_detail': ['harvest_id']
    }
    return column_name in skip_rules.get(table_name, [])

def import_csv_to_table(csv_file, db_path):
    """Importa el CSV adaptándose a la estructura de la tabla"""
    table_name = get_table_name_from_csv(csv_file)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            # Filtrar columnas a omitir
            filtered_headers = [h for h in headers if not should_skip_column(table_name, h)]
            col_indices = [i for i, h in enumerate(headers) if not should_skip_column(table_name, h)]
            
            # Construir consulta
            columns = ', '.join(filtered_headers)
            placeholders = ', '.join(['?'] * len(filtered_headers))
            query = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            # Procesar filas
            for row in reader:
                try:
                    # Filtrar columnas y manejar campos vacíos
                    filtered_row = [row[i] if i < len(row) else '' for i in col_indices]
                    cursor.execute(query, filtered_row)
                except Exception as row_error:
                    print(f"    - Error en fila {reader.line_num}: {str(row_error)}")
                    continue
        
        conn.commit()
        return table_name
        
    except Exception as e:
        print(f"  - Error importando {csv_file.name}: {str(e)}")
        return None
    finally:
        conn.close()

def main():
    project_root = Path(__file__).parents[2]
    db_path = project_root / "database" / "13cc.db"
    schema_path = project_root / "meta" / "schema.sql"
    exports_dir = project_root / "archive" / "exports"
    
    print("\nIniciando importación mejorada...")
    
    create_database_from_schema(db_path, schema_path)
    csv_files = get_csv_files(exports_dir)
    
    if not csv_files:
        print("\nNo se encontraron archivos CSV para importar")
        return
    
    print(f"\nImportando {len(csv_files)} archivos:")
    
    success_count = 0
    for csv_file in csv_files:
        print(f"\nProcesando: {csv_file.name}")
        table_name = import_csv_to_table(csv_file, db_path)
        if table_name:
            print(f"  ✓ Importado a tabla '{table_name}'")
            success_count += 1
    
    print(f"\nResumen final: {success_count}/{len(csv_files)} archivos importados")

if __name__ == "__main__":
    main()

"""
## Cambios Clave:

1. **Manejo de IDs redundantes**:
   - Omite automáticamente `harvest_id` cuando importa a las tablas `harvest` y `harvest_detail`

2. **Mejor manejo de errores**:
   - Identifica el número de línea con errores en los CSV
   - Continúa con las filas válidas aunque algunas fallen

3. **Procesamiento más robusto**:
   - Filtrado de columnas problemáticas
   - Manejo de campos vacíos o faltantes

4. **Información detallada**:
   - Muestra qué archivo se está procesando actualmente
   - Informa errores específicos por fila

## Recomendaciones Finales:

1. Verifica que los archivos CSV problemáticos no tengan:
   - Filas vacías al final
   - Campos con comas no escapadas
   - Encabezados mal formados

2. Para inspeccionar los CSV:
```bash
# Ver las primeras líneas del CSV problemático
head -n 5 archive/exports/harvest_20250813_171746.csv

# Verificar número de columnas
awk -F, '{print NF}' archive/exports/harvest_20250813_171746.csv | sort -nu
```

3. Si persisten los problemas, considera:
   - Exportar nuevamente los datos desde la base de datos original
   - Verificar que el schema.sql coincida con la estructura esperada
"""
