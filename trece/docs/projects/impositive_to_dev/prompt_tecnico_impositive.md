# 🧩 **PROMPT TÉCNICO - Sistema Trece Impositive v0.1.0**

## 📋 **CONTEXTO DEL SISTEMA**

**Proyecto:** ONG 13 Cannabis Club - Sistema de gestión integral  
**Objetivo:** Registro de socios, proveedores, cosechas, retiros, gastos y control de stock  
**Tecnologías:** Python 3.11, SQLite, Typer (CLI), Docker  
**Estado:** ✅ Sistema completo funcionando

---

## 🗃️ **ESQUEMA SQLite - EXPLICACIÓN DETALLADA**

### **Tablas Principales de Entidades**

#### `entity_types` - Tipos de entidades
```sql
CREATE TABLE entity_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,  -- 'socio', 'proveedor', 'empleado'
    description TEXT
);
```

#### `entities` - Entidades principales
```sql
CREATE TABLE entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,              -- Nombre completo
    entity_type_id INTEGER NOT NULL, -- FK a entity_types
    email TEXT, phone TEXT, address TEXT,
    membership_number TEXT UNIQUE,   -- N° de socio único
    status TEXT DEFAULT 'active'
);
```
**Relación:** Una entidad pertenece a un tipo (socio/proveedor/empleado)

### **Tablas de Productos y Cultivo**

#### `genetics` - Genéticas de cannabis
```sql
CREATE TABLE genetics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,       -- 'OG Kush', 'Blue Dream'
    description TEXT,
    thc_range TEXT, cbd_range TEXT,  -- Rangos de cannabinoides
    flowering_days INTEGER,          -- Días de floración
    status TEXT DEFAULT 'active'
);
```

#### `modules` - Módulos de cultivo
```sql
CREATE TABLE modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,       -- 'Módulo 1', 'Invernadero'
    capacity_plants INTEGER,         -- Capacidad en plantas
    capacity_grams INTEGER           -- Capacidad en gramos
);
```

### **Sistema de Precios**

#### `prices` - Precios históricos
```sql
CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genetic_id INTEGER NOT NULL,     -- FK a genetics
    price_per_gram DECIMAL(10,2) NOT NULL, -- Precio por gramo
    start_date DATE NOT NULL,        -- Fecha de inicio de vigencia
    end_date DATE,                   -- Fecha de fin (NULL = vigente)
    FOREIGN KEY (genetic_id) REFERENCES genetics(id)
);
```
**Regla de negocio:** Solo un precio vigente por genética

### **Operaciones Principales**

#### `harvests` & `harvest_items` - Cosechas
```sql
-- Cosecha principal
CREATE TABLE harvests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,      -- Módulo donde se cosechó
    harvest_date DATE NOT NULL,
    total_grams DECIMAL(10,2) NOT NULL, -- Total de la cosecha
    status TEXT DEFAULT 'completed'
);

-- Items por genética
CREATE TABLE harvest_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    harvest_id INTEGER NOT NULL,     -- FK a harvests
    genetic_id INTEGER NOT NULL,     -- Genética cosechada
    grams DECIMAL(10,2) NOT NULL,    -- Gramos de esta genética
    quality_notes TEXT,
    FOREIGN KEY (harvest_id) REFERENCES harvests(id),
    FOREIGN KEY (genetic_id) REFERENCES genetics(id),
    UNIQUE(harvest_id, genetic_id)   -- Una genética por cosecha
);
```

#### `withdrawals` - Retiros (ventas a socios)
```sql
CREATE TABLE withdrawals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,      -- Socio que retira
    genetic_id INTEGER NOT NULL,     -- Genética retirada
    grams DECIMAL(10,2) NOT NULL,
    price_per_gram DECIMAL(10,2) NOT NULL, -- Precio al momento del retiro
    total_amount DECIMAL(10,2) NOT NULL,   -- grams * price_per_gram
    withdrawal_date DATE NOT NULL,
    status TEXT DEFAULT 'completed', -- 'pending', 'completed', 'canceled'
    notes TEXT,
    FOREIGN KEY (entity_id) REFERENCES entities(id),
    FOREIGN KEY (genetic_id) REFERENCES genetics(id)
);
```

#### `expenses` - Gastos operativos
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,      -- Proveedor
    concept_id INTEGER NOT NULL,     -- Tipo de gasto
    amount DECIMAL(15,2) NOT NULL,
    expense_date DATE NOT NULL,
    folio TEXT,                      -- N° de factura/recibo
    paymethod_id INTEGER,            -- Método de pago
    notes TEXT,
    status TEXT DEFAULT 'completed',
    FOREIGN KEY (entity_id) REFERENCES entities(id),
    FOREIGN KEY (concept_id) REFERENCES concepts(id),
    FOREIGN KEY (paymethod_id) REFERENCES paymethods(id)
);
```

### **Sistema de Stock**

#### `stock_movements` - Trazabilidad completa
```sql
CREATE TABLE stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genetic_id INTEGER NOT NULL,
    movement_type TEXT NOT NULL,     -- 'in' (entrada), 'out' (salida)
    quantity DECIMAL(10,2) NOT NULL,
    reference_table TEXT NOT NULL,   -- 'harvest_items', 'withdrawals'
    reference_id INTEGER NOT NULL,   -- ID en la tabla referenciada
    movement_date DATE NOT NULL,     -- Fecha del movimiento
    notes TEXT
);
```
**Cálculo de stock:** `SUM(entradas) - SUM(salidas)` por genética

### **Tablas de Configuración**

#### `concepts` - Conceptos de gastos
```sql
CREATE TABLE concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,       -- 'fertilizantes', 'electricidad'
    description TEXT,
    category TEXT                    -- 'cultivo', 'operacion'
);
```

#### `paymethods` - Métodos de pago
```sql
CREATE TABLE paymethods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,       -- 'efectivo', 'transferencia', 'tarjeta'
    description TEXT
);
```

#### `cajas` - Control de efectivo
```sql
CREATE TABLE cajas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,       -- 'caja_principal'
    balance DECIMAL(15,2) DEFAULT 0.00
);
```

---

## 🐍 **ARQUITECTURA PYTHON - MÓDULOS PRINCIPALES**

### **`db.py` - Gestor de Base de Datos**
```python
class DatabaseManager:
    # Conexión SQLite con WAL para mejor concurrencia
    # Manejo automático de transacciones
    # Configuración centralizada via config.yaml
```

**Funciones clave:**
- `get_connection()` - Conexión con WAL habilitado
- `execute()` - Ejecución con commit automático
- `fetchone()/fetchall()` - Consultas con resultados
- `insert_and_get_id()` - Inserción con retorno de ID

### **Módulos de Carga (`load_*.py`)**

#### Patrón común:
1. **Validación de existencia** por nombres (no IDs)
2. **Creación automática** de registros relacionados
3. **Registro de movimientos** de stock
4. **Manejo de errores** con logging detallado

#### `load_entities.py`
- Creación de socios/proveedores
- Gestión automática de `entity_types`

#### `load_genetics.py` 
- Registro de genéticas con metadatos
- Validación de nombres únicos

#### `load_harvest.py`
- Cosechas con items por genética
- Registro automático de stock de entrada
- Gestión de módulos de cultivo

#### `load_withdrawal.py`
- Validación de stock disponible
- Cálculo automático de montos
- Registro de stock de salida
- **Requerimiento:** Precios definidos previamente

#### `load_expense.py`
- Gastos con proveedores
- Gestión de conceptos y métodos de pago
- Soporte para folios/comprobantes

### **Sistema de Reportes (`reports.py`)**

#### `generate_balance_report()`
- Cálculo mensual de ingresos/egresos
- Detalle de movimientos con `--detailed`
- Agrupación por mes (formato YYYY-MM)

#### `generate_stock_report()`
- Stock actual por genética
- Filtrado por nombre o ID
- Cálculo: `SUM(entradas) - SUM(salidas)`

### **Gestión de Stock (`stock.py`)**

#### `rebuild_stock()`
- Reconstrucción completa desde tablas base
- Útil después de importaciones masivas
- Mantiene consistencia de datos

#### `get_stock_summary()`
- Resumen consolidado por genética
- Total entradas/salidas/disponible

---

## 🚀 **FLUJOS DE TRABAJO PRINCIPALES**

### **1. Configuración Inicial**
```bash
trece init                          # Inicializar BD
trece load entities --name "Admin" --entity-type "empleado"
trece load genetics --name "OG Kush" --thc-range "15-25%"
trece load prices --genetic "OG Kush" --price 5000
```

### **2. Ciclo Operativo Mensual**
```bash
# Registrar cosechas
trece load harvest --genetic "OG Kush" --grams 500 --date "2024-01-15" --module "Modulo 1"

# Registrar retiros a socios  (forma correcta)
trece load withdrawal --entity "Juan Perez" --genetic "OG Kush" --grams 10 --date "2024-01-20"

# Registrar gastos
trece load expense --entity "Proveedor Verde" --amount 1500 --concept "fertilizantes" --date "2024-01-25"

# Generar reportes
trece report balance 2024-01 --detailed
trece report stock
```

### **3. Mantenimiento**
```bash
trece rebuild-stock                # Reconstruir stock si hay inconsistencias
```

---

## ⚠️ **REGLAS DE NEGOCIO CRÍTICAS**

1. **Stock:** Validación automática antes de retiros
2. **Precios:** Deben definirse antes de los retiros
3. **Nombres:** Usar nombres en lugar de IDs en CLI
4. **Fechas:** Formato YYYY-MM-DD en todos los comandos
5. **Movimientos:** Stock se actualiza automáticamente

---

## 🔧 **ESTRUCTURA DE ARCHIVOS**
```
trece/
├── config/config.yaml             # Configuración central
├── database/trece.db              # Base de datos SQLite
├── meta/schema.sql                # Esquema de base de datos
└── src/core/impositive/
    ├── impositive.py              # CLI principal (Typer)
    └── command/
        ├── db.py                  # Gestor de base de datos
        ├── load_entities.py       # Carga de socios/proveedores
        ├── load_genetics.py       # Carga de genéticas
        ├── load_harvest.py        # Registro de cosechas
        ├── load_withdrawal.py     # Registro de retiros
        ├── load_expense.py        # Registro de gastos
        ├── load_prices.py         # Definición de precios
        ├── reports.py             # Generación de reportes
        └── stock.py               # Gestión de stock
```

---

**¿Listo para implementar?** El sistema está completo y funcional para producción.