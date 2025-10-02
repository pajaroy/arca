# ✅ Sprint - Integración de Librerías para ARCA

**Versión:** 0.1.0  
**Autor:** Bird  
**Fecha:** 2025-07-16

---

## 🚀 Objetivo

Construir un **sistema gestor de archivos sólido, modular y trazable** para ARCA, sobre el cual se puedan desarrollar nuevos módulos internos (ML, RAG, etc.), integrando las siguientes librerías:

- blake3
- ruamel.yaml
- sqlite3
- chroma
- scikit-learn
- numpy
- pandas
- joblib
- loguru
- typer
- rich
- pytest

---

## ✅ Estructura Base del Proyecto

```
/arca/
    main.py
    config/
    utils/
    models/
    cli/
    tests/
requirements.yaml
contexto.yaml
```

---

## ✅ Sprint de Integración - Paso a Paso

### 1️⃣ Gestión de Archivos

**Librerías:**
- pathlib
- loguru

**Tareas:**
- Crear, borrar, mover archivos.
- Loguear cada acción realizada.

**Ejemplo:**

```python
from pathlib import Path
from loguru import logger

def crear_archivo(path, content=""):
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)
    logger.info(f"Archivo creado: {file}")
```

---

### 2️⃣ Hashing para Integridad

**Librería:**
- blake3

**Tareas:**
- Calcular hash para archivos.
- Guardar hash en metadatos o índices.

**Ejemplo:**

```python
from blake3 import blake3

def calc_hash(path):
    hasher = blake3()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
```

---

### 3️⃣ Configuración y Metadata

**Librería:**
- ruamel.yaml

**Tareas:**
- Leer archivos de configuración.
- Generar frontmatter YAML para cada archivo.

**Ejemplo:**

```python
from ruamel.yaml import YAML

yaml = YAML()

def load_config(path):
    with open(path) as f:
        return yaml.load(f)
```

---

### 4️⃣ Indexación y Base de Datos

**Librería:**
- sqlite3

**Tareas:**
- Crear base de datos para:
    - paths
    - hashes
    - timestamps
- Actualizar índices tras cada operación.

**Ejemplo:**

```python
import sqlite3

def init_db():
    conn = sqlite3.connect("arca_index.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS archivos (
        id TEXT PRIMARY KEY,
        path TEXT,
        hash TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)
    conn.commit()
    conn.close()
```

---

### 5️⃣ CLI

**Librerías:**
- typer
- rich

**Tareas:**
- Crear comandos CLI para:
    - Crear archivos.
    - Listar índices.
    - Consultar logs.
- Usar rich para imprimir tablas y salidas bonitas.

**Ejemplo:**

```python
import typer
from rich import print
from rich.table import Table

app = typer.Typer()

@app.command()
def show_index():
    table = Table(title="Índice de Archivos")
    table.add_column("Path")
    table.add_column("Hash")
    print(table)

if __name__ == "__main__":
    app()
```

---

### 6️⃣ ML Base

**Librerías:**
- scikit-learn
- numpy
- pandas
- joblib

**Tareas:**
- Preparar datasets (logs, histórico de archivos).
- Entrenar modelos ML:
    - Clasificación
    - Anomalías
- Guardar modelos entrenados para futuras predicciones.

**Ejemplo:**

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Simulamos datos
df = pd.DataFrame({
    "size": [100, 200, 150],
    "is_markdown": [1, 0, 1]
})

X = df[["size"]]
y = df["is_markdown"]

clf = RandomForestClassifier().fit(X, y)
joblib.dump(clf, "model.joblib")
```

---

### 7️⃣ RAG Preparado

**Librería:**
- chroma

**Tareas:**
- Estructurar integración para embeddings.
- Preparar almacenamiento en vector store.
- No implementar RAG completo todavía, solo la estructura para integrar futuro.

---

### 8️⃣ Testing

**Librería:**
- pytest

**Tareas:**
- Tests para:
    - Creación de archivos.
    - Hashing.
    - Base de datos.
    - CLI comandos.

**Ejemplo:**

```python
def test_crear_archivo(tmp_path):
    file = tmp_path / "test.md"
    crear_archivo(file, "Hola")
    assert file.read_text() == "Hola"
```

---

## ✅ Sprint Plan

| Día | Tarea |
|-----|-------|
| 1 | Inicializar repo, estructura carpetas, logging básico. |
| 2 | Implementar gestor de archivos (pathlib + loguru). |
| 3 | Hashing con blake3. |
| 4 | Configuración y YAML frontmatter. |
| 5 | Base de datos con sqlite3. |
| 6 | CLI inicial con typer. |
| 7 | Integrar rich en CLI. |
| 8 | Scripts de ML básico. |
| 9 | Configurar chroma (estructura inicial). |
| 10 | Escribir tests con pytest. |

---

## ✅ Resultado del Sprint

✅ Sistema gestor de archivos sólido.  
✅ Integridad y trazabilidad garantizadas.  
✅ CLI funcional y profesional.  
✅ Base lista para integrar ML y RAG.  
✅ Preparado para crecer con módulos internos en ALMA_RESIST.

---

**Fin del documento.**
