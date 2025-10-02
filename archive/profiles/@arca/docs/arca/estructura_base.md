# 📦 Scripts Base para Sistema Autocreable (ALMA_RESIST / Arca)

Este documento resume los **scripts fundamentales** que debe tener un entorno autocreable modular impulsado por IA. Cada módulo incluye:

- Propósito
- Enfoque de implementación
- Prompt recomendado para desarrollo asistido

---

## 1. `load_config.py`
**Propósito:** Cargar configuración YAML general del sistema.

**Implementación:** Usar `ruamel.yaml`, rutas absolutas o relativas desde `/config`.

**Prompt interno:**
```yaml
objetivo: Cargar configuración YAML del sistema desde ruta segura
librerías: ruamel.yaml, pathlib
output: diccionario con claves y valores de configuración
```

---

## 2. `load_schema.py`
**Propósito:** Cargar y validar schemas YAML de archivos/documentos.

**Implementación:** Mismo enfoque que config, estructura clara y minimalista.

**Prompt interno:**
```yaml
objetivo: Cargar y validar schemas YAML de documentos
librerías: ruamel.yaml, pathlib
output: estructura de schema usable por otros módulos
```

---

## 3. `hash_utils.py`
**Propósito:** Calcular hash de archivos o strings para integridad.

**Implementación:** Usar `blake3`, permitir input de rutas o strings directos.

**Prompt interno:**
```yaml
objetivo: Calcular hash de archivos o strings con blake3
librerías: blake3, pathlib
output: string hash único
```

---

## 4. `indexer.py`
**Propósito:** Crear, mantener y consultar índices de archivos.

**Implementación:** Soportar JSON y SQLite. Indexar UUID, hash, fecha, tipo, etc.

**Prompt interno:**
```yaml
objetivo: Crear índice y registrar documentos con metadatos clave
librerías: sqlite3, json, pathlib
output: índices consultables por CLI y módulos ML
```

---

## 5. `logger.py`
**Propósito:** Configurar logging estandarizado para todos los módulos.

**Implementación:** Usar `loguru`, formateo claro y archivo de salida rotativo.

**Prompt interno:**
```yaml
objetivo: Configurar sistema de logs con rotación y trazabilidad
librerías: loguru
output: archivo .log usable por auditoría
```

---

## 6. `file_manager.py`
**Propósito:** Operaciones básicas de archivos: crear, mover, eliminar, versionar.

**Implementación:** Usar `pathlib`, registrar todo en logs.

**Prompt interno:**
```yaml
objetivo: Crear y administrar archivos versionados con trazabilidad
librerías: pathlib, loguru
output: operaciones documentadas y reversibles
```

---

## 7. `cli.py`
**Propósito:** Crear CLI central para interactuar con el sistema.

**Implementación:** `typer` para comandos, `rich` para salida visual.

**Prompt interno:**
```yaml
objetivo: Crear CLI interactiva con comandos para Arca y ML
librerías: typer, rich
output: comandos funcionales y documentados
```

---

## 8. `ml_utils.py`
**Propósito:** Funciones para entrenar, guardar, cargar modelos ML.

**Implementación:** `scikit-learn`, `joblib`, validación previa de inputs.

**Prompt interno:**
```yaml
objetivo: Entrenar y reutilizar modelos ML para predicción documental
librerías: sklearn, joblib, pandas
output: modelos persistidos y reutilizables
```

---

## 9. `db.py`
**Propósito:** Acceso unificado a `sqlite3` y `chroma` para embeddings.

**Implementación:** Funciones CRUD básicas + conexión vector store.

**Prompt interno:**
```yaml
objetivo: Conectar y consultar SQLite + Chroma para almacenamiento mixto
librerías: sqlite3, chromadb
output: interfaz unificada para DB estructurada y vectorial
```

---

## 10. `tests/`
**Propósito:** Validar módulos críticos con `pytest`.

**Implementación:** 1 test mínimo por módulo funcional.

**Prompt interno:**
```yaml
objetivo: Validar funciones clave de cada módulo en entorno aislado
librerías: pytest
output: validación continua y trazable
```

---
