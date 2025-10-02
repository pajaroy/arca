## 🌐 Visión General
Estructura modular para la gestión de datos, metadatos y agentes inteligentes.  
**Principios**:  
- 🔒 **Inmutabilidad**: Los archivos fuente nunca se modifican directamente.  
- 🧠 **Trazabilidad**: Todo dato procesado puede rastrearse hasta su origen.  
- 🏗️ **Modularidad**: Componentes independientes pero integrables.  
- 📊 **Centralización**: Una base maestra (`database/`) concentra todo el conocimiento persistente.  

---

## 📂 Estructura de Directorios

### 🔍 Carpetas Principales (Visibles)
| Carpeta       | Propósito                                                                    |
|---------------|------------------------------------------------------------------------------|
| `config/`     | Configuraciones globales y por módulo                                        |
| `core/`       | Motor central: utilidades, procesamiento, ML/RAG (`core/ml`)                 |
| `data/`       | Datos crudos, temporales o procesados fuera de bases persistentes            |
| `database/`   | Almacenamiento persistente: SQL, índices vectoriales, metadatos              |
| `modules/`    | Agentes o bloques de trabajo (extensiones funcionales)                       |
| `meta/`       | Esquemas, modelos de datos y documentación estructural                       |
| `logs/`       | Registros de ejecución y auditoría                                           |
| `templates/`  | Plantillas para módulos, metadatos y configuraciones                         |

---

## 🔄 Flujo de Datos

```mermaid
graph LR
    A[data/raw/] -->|Normalización| B[data/processed/]
    B -->|Indexación/Embeddings| C[database/vector_index]
    B -->|Carga| D[database/arca.db]
    C -->|Búsqueda Semántica| E[core/ml]
    D -->|Consultas| E
    E -->|Respuestas| F[modules/agentes]
````

---

## 🛠️ Uso Básico

### 1. Ingresar archivos nuevos

```bash
# Copiar preservando metadatos
cp -p informe.pdf ~/@arca/data/raw/proyecto_alma/$(date +%Y%m%d)_informe.pdf
```

### 2. Procesar datos y generar embeddings

```python
from pathlib import Path
from core.config import paths
from core.ml.embedding import generar_embedding

ruta_fuente = paths.DATA_RAW / "proyecto_alma/20240203_informe.pdf"
vector = generar_embedding(ruta_fuente)
```

### 3. Generar reportes desde la base maestra

```bash
nix-shell --run "python modules/reportes/generar_reporte.py"
```

---

## 📌 Reglas de Oro

1. **Nunca** modificar datos crudos en `data/raw/` directamente.
2. Prefijar archivos con `YYYYMMDD_` para control temporal.
3. Documentar cambios estructurales en `./CHANGELOG.md`.
4. Justificar decisiones técnicas en `./doc/decisiones.md`.
5. El **core** es el único autorizado a escribir en `database/`.

---

