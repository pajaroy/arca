Acá tenés los comandos esenciales para ver datos en SQLite:

## 🔍 **COMANDOS BÁSICOS SQLite**

### **1. Entrar a la base de datos:**
```bash
sqlite3 database/trece.db
```

### **2. Ver todas las tablas:**
```sql
.tables
```

### **3. Ver estructura de una tabla:**
```sql
.schema entities
.schema genetics
.schema withdrawals
```

### **4. Ver datos de tablas:**
```sql
-- Ver todas las entidades
SELECT * FROM entities;

-- Ver entidades con sus tipos
SELECT e.id, e.name, et.name as tipo 
FROM entities e 
JOIN entity_types et ON e.entity_type_id = et.id;

-- Ver genéticas
SELECT * FROM genetics;

-- Ver retiros con nombres
SELECT w.id, e.name as socio, g.name as genetica, w.grams, w.total_amount, w.withdrawal_date
FROM withdrawals w
JOIN entities e ON w.entity_id = e.id
JOIN genetics g ON w.genetic_id = g.id;

-- Ver gastos con nombres
SELECT exp.id, e.name as proveedor, c.name as concepto, exp.amount, exp.expense_date
FROM expenses exp
JOIN entities e ON exp.entity_id = e.id
JOIN concepts c ON exp.concept_id = c.id;

-- Ver stock actual por genética
SELECT g.name, 
       SUM(CASE WHEN sm.movement_type = 'in' THEN sm.quantity ELSE 0 END) as entradas,
       SUM(CASE WHEN sm.movement_type = 'out' THEN sm.quantity ELSE 0 END) as salidas,
       SUM(CASE WHEN sm.movement_type = 'in' THEN sm.quantity ELSE -sm.quantity END) as stock
FROM genetics g
LEFT JOIN stock_movements sm ON g.id = sm.genetic_id
GROUP BY g.id, g.name;
```

### **5. Comandos útiles de formato:**
```sql
.headers on        -- Mostrar nombres de columnas
.mode column       -- Formato columnas
.width 20 15 10    -- Ancho de columnas
```

### **6. Consultas específicas útiles:**
```sql
-- Ver movimientos de stock recientes
SELECT g.name, sm.movement_type, sm.quantity, sm.movement_date, sm.reference_table
FROM stock_movements sm
JOIN genetics g ON sm.genetic_id = g.id
ORDER BY sm.movement_date DESC
LIMIT 10;

-- Ver precios vigentes
SELECT g.name, p.price_per_gram, p.start_date
FROM prices p
JOIN genetics g ON p.genetic_id = g.id
WHERE p.end_date IS NULL OR p.end_date >= date('now');

-- Balance del último mes
SELECT 
  SUM(CASE WHEN strftime('%Y-%m', withdrawal_date) = '2024-01' THEN total_amount ELSE 0 END) as ingresos,
  SUM(CASE WHEN strftime('%Y-%m', expense_date) = '2024-01' THEN amount ELSE 0 END) as gastos
FROM withdrawals, expenses;
```

### **7. Salir de SQLite:**
```sql
.quit
```

## 🐍 **DESDE PYTHON también podés ver datos:**
```python
# En el contenedor, probá:
python -c "
from src.core.impositive.command.db import db_manager
result = db_manager.fetchall('SELECT name FROM entities')
print('Entidades:', [r['name'] for r in result])
"
```

## 📊 **EJEMPLO PRÁCTICO - Verificar carga:**
```bash
# Entrar a la BD
sqlite3 database/trece.db

# Verificar que se cargaron los datos
.headers on
.mode column

SELECT '=== ENTIDADES ===';
SELECT * FROM entities LIMIT 5;

SELECT '=== GENÉTICAS ===';  
SELECT * FROM genetics LIMIT 5;

SELECT '=== STOCK ACTUAL ===';
SELECT g.name, 
       SUM(CASE WHEN sm.movement_type = 'in' THEN sm.quantity ELSE 0 END) -
       SUM(CASE WHEN sm.movement_type = 'out' THEN sm.quantity ELSE 0 END) as stock
FROM genetics g
LEFT JOIN stock_movements sm ON g.id = sm.genetic_id
GROUP BY g.id;
```

**¿Querés que probemos ver algún dato específico de tu base?**