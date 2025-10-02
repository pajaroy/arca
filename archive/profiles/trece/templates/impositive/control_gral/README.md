# 📋 **Template de Control de Retiros - Manual de Uso**  

### **🔹 Descripción**  
Este archivo Excel está diseñado para llevar un **control preciso** de retiros de genéticas, calculando automáticamente:  
- Stock disponible por genética.  
- Dinero total generado.  
- Resúmenes generales.  

---

## **📂 Estructura del Archivo**  
### **1. Hoja `stock`**  
#### **Qué contiene:**  
- **Genética**: Nombre de la variedad (ej: "Chendawg", "OG Kush").  
- **Módulo**: Ubicación (ej: "A-1", "B-2").  
- **Stock inicial**: Cantidad inicial cargada.  
- **Retiro total**: Suma de retiros (se calcula automáticamente).  
- **Stock disponible**: Stock inicial - Retiro total.  
- **Dinero total**: Suma de ingresos por genética.  

#### **Cómo cargar datos:**  
1. Ingresar manualmente:  
   - **Genética** (ej: "Chendawg").  
   - **Stock inicial** (ej: 100).  
2. **Fórmulas preconfiguradas** (no modificar):  
   - **Retiro total (columna D)**:  
     ```excel
     =SUMIF($retiros.B2:B1200, "x", $retiros.D2:D1200)
     ```  
     *(Reemplazar `"x"` por el nombre exacto de la genética, ej: `"Chendawg"`)*.  
   - **Dinero total (columna F)**:  
     ```excel
     =SUMIF($retiros.B2:B1200, "x", $retiros.F2:F1200)
     ```  
     *(Igual que arriba, reemplazar `"x"`)*.  

---

### **2. Hoja `retiros`**  
#### **Qué contiene:**  
- **Fecha**: Fecha del retiro (formato: `YYYY-MM-DD`).  
- **Genética**: Nombre de la variedad (debe coincidir con `stock`).  
- **Paciente**: Nombre del cliente (opcional).  
- **Cantidad**: Unidades retiradas.  
- **Precio unitario**: Precio por unidad (ajustar manualmente si varía).  
- **Precio total**: `=Cantidad * Precio unitario` (automático).  
- **Método de pago**: Efectivo, transferencia, etc.  

#### **Cómo cargar datos:**  
1. Solo completar las columnas:  
   - **Fecha**, **Genética**, **Paciente**, **Cantidad**, **Método de pago**.  
2. El resto se calcula solo.  

---

### **3. Hoja `resumen_gral`**  
#### **Qué contiene:**  
- **Total ingresado**: Suma de todo el stock inicial.  
- **Total retirado**: Suma de todos los retiros.  
- **Total disponible**: Stock inicial - Retiros.  
- **Dinero total generado**: Suma de todos los `precio_total`.  

#### **Fórmulas (no tocar):**  
```excel
=SUMIF($stock.B$2:B$100, "A-1", $stock.C$2:C$100)  // Total ingresado (stock inicial)
=SUMIF($stock.B$2:B$100, "A-1", $stock.D$2:D$100)  // Total retirado
=C2-D2  // Total disponible
=SUMIF($stock.B$2:B$100, "A-1", $stock.F$2:F$100)  // Dinero total
```

---

## **🚀 Recomendaciones**  
1. **Nombres consistentes**:  
   - Escribir las genéticas **igual** en `stock` y `retiros` (ej: "Chendawg" ≠ "chendawg").  
2. **Actualizar siempre**:  
   - Al agregar retiros, verificar que `resumen_gral` se actualice.  
3. **Copias de seguridad**:  
   - Guardar una versión al final del día.  

---


## Explicacion a mano

Template de control general de retiros.
Consta de 3 hojas: retiros, stock, y resumen_gral

Se comienza cargando en la hoja stock por genetica y cantidad, lo cual nos dara el resumen general.

Dentro de la hoja stock al agregar la genetica reemplazar en las columnas 'D: "=SUMIF($retiros.B2:B1200, "x", $retiros.D2:D1200)" y en F: "=SUMIF($retiros.B2:B1200, "x", $retiros.F2:F1200)" Reemplazar la x por el nombre de la genetica en ambos casos, esto permitira contar por genetica el retiro_total y el total del dinero generado por genetica.

Dentro de la hoja retiros solo se debe agregar fecha, paciente y cantidad , el resto se calcula automaticamente y se refleja en las demas hojas

---