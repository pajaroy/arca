# 📋 **Listado Completo de Comandos Trece Impositive**

## 🏗️ **COMANDOS DE INICIALIZACIÓN**

### `trece init`
Inicializar base de datos
```bash
trece init
```

### `trece version`
Mostrar versión del sistema
```bash
trece version
```

### `trece rebuild-stock`
Reconstruir movimientos de stock desde cero
```bash
trece rebuild-stock
```

## 📥 **COMANDOS DE CARGA DE DATOS**

### **Entidades (Socios/Proveedores)**
```bash
# Desde CSV
trece load entities archivo.csv

# Directo
trece load entities --name "Nombre" --entity-type "socio|proveedor|empleado" [--email "email@ejemplo.com"] [--phone "123456789"] [--address "Dirección"] [--membership-number "ABC123"]
```

### **Genéticas**
```bash
# Desde CSV
trece load genetics archivo.csv

# Directo  
trece load genetics --name "Nombre Genética" [--description "Descripción"] [--thc-range "15-25%"] [--cbd-range "0-1%"] [--flowering-days 60]
```

### **Cosechas**
```bash
# Desde CSV
trece load harvest archivo.csv

# Directo
trece load harvest --genetic "Nombre Genética" --grams 500 --date "YYYY-MM-DD" --module "Nombre Módulo" [--quality-notes "Notas de calidad"]
```

### **Retiros (Ventas a socios)**
```bash
# Desde CSV
trece load withdrawal archivo.csv

# Directo (no funciona)
trece load withdrawal --entity "Nombre Socio" --genetic "Nombre Genética" --grams 10 --date "YYYY-MM-DD" [--price-per-gram 5000] [--notes "Notas"] 
```

### **Gastos**
```bash
# Desde CSV  
trece load expense archivo.csv

# Directo
trece load expense --entity "Nombre Proveedor" --amount 1500 --concept "concepto" --date "YYYY-MM-DD" [--folio "FAC-001"] [--paymethod "efectivo|transferencia|tarjeta"] [--notes "Notas"]
```

### **Precios** (Nuevo - necesario para retiros)
```bash
# Desde CSV
trece load prices archivo.csv

# Directo
trece load prices --genetic "Nombre Genética" --price 5000 [--date "YYYY-MM-DD"]
```

## 📊 **COMANDOS DE REPORTES**

### **Balance Mensual**
```bash
trece report balance YYYY-MM [--detailed]
# Ejemplo: trece report balance 2024-01 --detailed
```

### **Stock Actual**
```bash
trece report stock [--genetic "Nombre o ID Genética"]
# Ejemplos:
trece report stock
trece report stock --genetic "OG Kush"
trece report stock --genetic "1"
```

## 🗃️ **ESTRUCTURA DE ARCHIVOS CSV**

### **entities.csv**
```csv
name,entity_type,email,phone,address,membership_number
"Juan Perez","socio","juan@email.com","123456789","Dirección 123","SOC-001"
"Proveedor Verde","proveedor","proveedor@verde.com","987654321","",""
```

### **genetics.csv**
```csv
name,description,thc_range,cbd_range,flowering_days
"OG Kush","Genética clásica","15-25%","0-1%",60
"Blue Dream","Híbrido balanceado","12-20%","0-2%",65
```

### **harvest.csv**
```csv
genetic,grams,harvest_date,module,quality_notes
"OG Kush",500.0,"2024-01-10","Módulo 1","Excelente calidad"
"Blue Dream",350.0,"2024-01-15","Módulo 2","Buena producción"
```

### **withdrawal.csv**
```csv
entity,genetic,grams,withdrawal_date,price_per_gram,notes
"Juan Perez","OG Kush",10.0,"2024-01-15",5000.0,"Retiro mensual"
"Maria Lopez","Blue Dream",5.0,"2024-01-20",4500.0,""
```

### **expense.csv**
```csv
entity,amount,concept,expense_date,folio,paymethod,notes
"Proveedor Verde",1500.0,"fertilizantes","2024-01-20","FAC-001","efectivo","Fertilizantes orgánicos"
"Servicios Eléctricos",800.0,"electricidad","2024-01-25","","transferencia","Pago mensual"
```

### **prices.csv**
```csv
genetic,price_per_gram,start_date
"OG Kush",5000.0,"2024-01-01"
"Blue Dream",4500.0,"2024-01-01"
```

## 🔄 **FLUJO RECOMENDADO DE USO**

1. **Inicializar:** `trece init`
2. **Cargar datos base:** `trece load entities`, `trece load genetics`, `trece load prices`
3. **Registrar operaciones:** `trece load harvest`, `trece load withdrawal`, `trece load expense`
4. **Generar reportes:** `trece report balance`, `trece report stock`

**¿Te sirve este listado o necesitás algún comando específico explicado con más detalle?**