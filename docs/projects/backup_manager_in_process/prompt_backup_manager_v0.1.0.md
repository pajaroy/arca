---
type: "prompt"
version: "0.1.0"
description: "pedido para el script para el manejo de backups dentro de Arca"
---

# prompt\_backup\_manager\_v0.1.0

El **Backup Manager 0.1.0** es el encargado de la gestión de copias de seguridad dentro del ecosistema **arca**, funcionando **siempre dentro del contenedor Docker**, con `/arca/` como raíz absoluta del sistema.

Todas las rutas y parámetros se declaran en un archivo de configuración externo (`config.yaml`), para permitir una futura adaptación flexible sin modificar el código fuente.
El `max_backups` se manejará directamente desde el script.

---

## 📂 Estructura de proyecto

```
/arca/src/core/manager
├── README.md
├── backup
│   ├── README.md
│   └── main.py
└── config.yaml
```

---

## 📝 Configuración de ejemplo (`config.yaml`)

```yaml
version: "0.2.0"
author: "bird"

root: /arca

paths:
  archive: /arca/archive
  backup: /arca/archive/backup
  history: /arca/archive/history

meta:
  supported_extensions:
    - .yaml
    - .yml
    - .md
    - .json
    - .py
    - .csv
```

* `paths.backup` → donde se guardarán los backups.
* `paths.archive` → carpeta general de archivos de Arca.
* `paths.history` → historial o registros adicionales.
* `meta.supported_extensions` → extensiones de archivos a incluir por defecto.

---

## 🎯 Objetivos principales

1. **Gestionar backups de archivos y directorios arbitrarios**, preservando la estructura original dentro de `/arca/`.
2. **Automatizar la creación, listado y restauración** de backups.
3. **Mantener un número máximo de backups por archivo** (`max_backups`, manejado desde el script).
4. **Separar configuración en `config.yaml`** (rutas, extensiones, defaults).
5. **Controlar todo desde la línea de comandos** con `argparse`.
6. **Mantener trazabilidad mediante `logger`** con configuración centralizada.

---

## 🔧 Funciones principales

### 1. Crear backup

* Usar `pathlib` para resolver rutas.

* Generar backup comprimido (`.tar.gz`) de archivos o directorios seleccionados.

* Guardar en:

  ```
  {paths.backup}/{estructura_original}/{nombre}_{timestamp}.tar.gz
  ```

* Mantener el árbol de directorios igual al original.

* Permitir descripción opcional (`--desc`).

* Rotación automática (`max_backups` definida en script).

* Registrar acciones con `logger`.

### 2. Listar backups

* Mostrar backups existentes con metadatos: ruta original, fecha, tamaño, descripción.
* Salida en texto plano o JSON (`--json`).
* Registrar operaciones con `logger`.

### 3. Restaurar backup

* Restaurar backup por ruta absoluta o relativa.
* Opción de destino alternativo (`--target`).
* Confirmar antes de sobrescribir.
* Registrar con `logger.warning` cuando sobrescriba archivos.

---

## 🐍 Interfaz CLI

Ejemplos:

```bash
# Crear backup
python3 main.py create /arca/src/data --desc "Backup inicial" --max 5

# Listar backups
python3 main.py list --json

# Restaurar backup
python3 main.py restore /arca/archive/backup/src/data/file_2025-09-24_01-00-00.tar.gz --target /arca/tmp/test_restore
```

---

## 📜 Requisitos técnicos

* Python 3.
* `argparse` para CLI.
* `pathlib` para rutas.
* `logging` con `logger = logging.getLogger(__name__)`.
* Configuración en `config.yaml` (rutas, extensiones, defaults).
* Compresión/descompresión con `tarfile` + `gzip`.
* Compatible con extensiones definidas en `meta.supported_extensions`.

---

## 🚧 Limitaciones (v0.1.0)

* Solo backups completos.
* Sin verificación de integridad.
* Sin permisos avanzados.

---

## 🛠 Futuras mejoras (0.2.x+)

* Backups incrementales.
* Verificación de integridad (`blake3`).
* Políticas de retención avanzadas.
* Notificaciones integradas en **arca**.
* Configuración avanzada en `config.yaml`.

---

Si querés, el siguiente paso sería armar el **esqueleto de `main.py`** con `argparse`, `pathlib` y `logger` ya integrados, listo para leer esta config y gestionar los backups.

¿Querés que haga eso ahora?
