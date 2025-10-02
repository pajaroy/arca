# Bitacora Personal

## 2025-07-17 Inicio del sistema :

### 1. Iniciamos el sistema cargando todo desde un bash

Ubicación: ~/arca/init_arca.sh

### 2 .Creamos el script para cargar config.yaml 

Ubicación: ~/@arca/utils/load_config.py

### 3. Creamos el script para ignorar '.dev' y '.env'

Ubicación: ~/@arca/utils/should_ignore.py

### 4. Creamos el script para carga schemas 'load_schema.py'

Ubicación: ~/@arca/utils/load_schema.py

### 5. Definicion de Schemas. 

Se decidio modularizar los schemas.

#### 5.1 'frontmatter.yaml y frontmatter.sql'

Schema yaml: metadatos base para frontmatter
Ubicación: ~/@arca/meta/frontmatter.yaml

Schema sql: metadatos base para frontmatter
Ubicación: ~/@arca/meta/frontmatter.sql

#### 5.2 Schema para log YAML y sql

Schema: YAML
Ubicación: ~/@arca/meta/log.yaml

Schema : sql
Ubicación: ~/@arca/meta/log.sql

#### 5.x Template

Schema: [tipo] (YAML/sql)
Ubicación: ~/@arca/meta/

### 6. Creacion del script: 'hash_utils.py'

Calcula hash con blake3

Ubicación: ~/@arca/utils/hash_utils.py

### 7. Hashing e indexado

#### 7.1. init_index.py — crea la tabla si no existe

Ubicación: ~/@arca/utils/init_index.py

#### 7.2. indexar_documento.py — inserta o actualiza un documento

Ubicación: ~/@arca/utils/indexar_documento.py

### 8. utils/logger.py — versión con soporte a DB

Ubicación: ~/@arca/utils/logger.py

### 9. 'uuid_utils.py' Calcular uuid de un archivo.

Ubicación: ~/@arca/utils/uuid_utils.py


### 10. 'file_manager.py' creador de archivos

Ubicación: ~/@arca/utils/file_manager.py

### 11. 'test_flujo_creacion.py'

Test del flujo hasta file_manager.py
Ubicación: ~/@arca/tests/test_flujo_creacion.py

Debugeado y estable.