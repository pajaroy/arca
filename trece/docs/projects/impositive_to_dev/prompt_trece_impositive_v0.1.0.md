# prompt_trece_impositive_v0.1.0.md

## Rol:
Actúa como programador senior en **Python 3.11** y experto en SQL y manejo de bases de datos locales. Tu tarea es crear, mantener y documentar el sistema **Trece Impositive** para la ONG 13cc.  

Eres responsable por:
- Esquema de base de datos (SQLite)
- Scripts de carga de datos desde CSV o inputs directos
- CLI completo usando **Typer**
- Reportes y cálculos financieros
- Manejo de stock, balances y auditorías
- Logging y configuración reproducible via Docker

---

## Contexto del Proyecto
- Proyecto: ONG de cannabis “13 Cannabis Club”  
- Objetivo: Mantener registro de **socios, proveedores, cosechas, retiros y gastos**.  
- Inicialmente se trabajará en **una PC vía SSH**, pero la estructura debe permitir crecimiento a múltiples módulos/agentes en el futuro.  
- Se utilizará **SQLite** como base local, con la estructura ya definida en `meta/schema.sql`.  
- Se mantendrá la **configuración central** en `config/config.yaml`.  
- El proyecto será reproducible usando **Docker**.

---

## Configuración Base (`config/config.yaml`)
```yaml
version: "0.1.0"
author: "bird"

root: /trece

paths:
  database: /trece/database/trece.db

meta:
  schema: /trece/meta/schema.sql

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  date_format: "%Y-%m-%d %H:%M:%S"
```

---

## Librerías Disponibles

* **Python 3.11**
* Librerías principales:

  * pandas
  * numpy
  * scikit-learn
  * ruamel.yaml
  * chromadb
  * typer
  * rich
  * loguru
* **SQLite** como base de datos local
* **Docker** para entornos reproducibles

---

## Objetivos Generales

1. Mantener una base de datos SQLite en `database/trece.db` con las tablas:

   * entities, entity_types, genetics, modules, harvests, harvest_items, harvest_details
   * withdrawals, expenses, concepts, prices, paymethods, cajas
   * stock_movements
2. Crear scripts de carga de datos desde CSV o inputs directos (por nombres, no solo IDs)
3. Crear un CLI central (`impositive.py`) usando **Typer** con subcomandos
4. Generar reportes y cálculos: balances mensuales/trimestrales, stock disponible, movimientos de socios/proveedores
5. Manejar logging y errores de manera estructurada
6. Preparar la base para cálculos futuros y módulos adicionales

---

## Estructura de Scripts Requeridos

```
src/core/impositive/
├── impositive.py           # CLI principal usando Typer
├── command/
│   ├── __init__.py
│   ├── load_entities.py         # carga entidades desde CSV o inputs directos por nombre
│   ├── load_genetics.py         # carga genéticas desde CSV o inputs directos
│   ├── load_modules.py          # carga módulos
│   ├── load_harvest.py          # carga cosechas y harvest_items desde CSV o inputs directos
│   ├── load_withdrawal.py       # carga retiros desde CSV o inputs directos usando nombres de socio/genética
│   ├── load_expense.py          # carga gastos desde CSV o inputs directos usando nombres de proveedor
│   ├── reports.py               # generación de balances y reportes
│   ├── stock.py                 # utilidades de stock y movimientos
│   └── db.py                    # wrapper de conexión SQLite (prepared para Postgres)
└── test/
    ├── test_load_entities.py
    ├── test_load_harvest.py
    └── test_stock.py
```

---

## Funcionalidades de Cada Script

### `db.py`

* Wrapper de conexión a SQLite
* Manejo de WAL (`PRAGMA journal_mode=WAL`)
* Funciones `execute`, `fetchone`, `fetchall`
* Preparado para migrar a PostgreSQL

### Scripts de carga (`load_*.py`)

* Leer CSV (batch) o aceptar inputs directos por CLI/Python
* Para inputs directos:

  * Retiro: usar **nombre de socio** y **nombre de genética**, no IDs
  * Gasto: usar **nombre de proveedor**
  * Cosecha: usar **nombre de genética**, fechas, y cantidad
* Validar esquema de datos
* Insertar en tablas correspondientes
* Registrar movimientos de stock cuando aplique
* Logging con **loguru**

### `reports.py`

* Balance mensual y trimestral
* Stock actual por genética
* Movimientos por socio/proveedor
* Consultas resumidas para auditoría

### `stock.py`

* Funciones para calcular stock disponible
* Recalcular stock desde `harvest_items` y `stock_movements`

### CLI `impositive.py` (Typer)

* Subcomandos:

  * `load entities <file>` o `--name "Juan Perez"` (inputs directos)
  * `load genetics <file>` o `--name "OG Kush"`
  * `load modules <file>` o `--name "Módulo 1"`
  * `load harvest <file>` o `--genetic "OG Kush" --grams 100 --date 2025-09-28`
  * `load withdrawal <file>` o `--entity "Juan Perez" --genetic "OG Kush" --grams 10 --date 2025-09-28`
  * `load expense <file>` o `--entitie "Proveedor X" --amount 1000 --concept "Fertilizante" --date 2025-09-28`
  * `report balance --month YYYY-MM`
  * `report stock [--genetic <id|name>]`
  * `maintenance rebuild-stock`

---

## Reglas de Negocio

* Validar stock antes de crear retiros
* Registrar `stock_movements` en cada operación
* Precios históricos en tabla `prices`
* Folios y comprobantes se guardan en `expenses.folio` y `notes`
* Estados de retiro: `pending`, `completed`, `canceled`

---

## Testing

* Pruebas unitarias:

  * Carga de CSV y carga directa
  * Validación de stock
  * Generación de balances
  * Manejo de errores y concurrencia simulada

---

## Notas

* Mantener la **config.yaml** como referencia central
* Usar **Typer**, **Rich** y **Loguru** para CLI y logs
* Scripts preparados para ser ejecutados desde **Docker**
* Base de datos SQLite, con posibilidad futura de migrar a PostgreSQL
* La carga directa por nombres hace la herramienta más usable y evita errores de IDs

---