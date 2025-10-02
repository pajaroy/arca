---
type: "prompt"
fecha: "2025-08-19"
version: "0.1.3"
descripcion: "Terminal contable 13cc"
---
**Solicitud de Terminal CLI Persistente para Gestión de Planillas CSV**

Necesito un terminal CLI interactivo y persistente que gestione cálculos sobre tablas CSV con la siguiente estructura y funcionalidades:

## 🎨 Diseño del Terminal:
- Muestra un "13" grande en ASCII art que permanezca visible siempre
- Interfaz colorida y organizada por secciones
- Prompt personalizado: `data_cli> `

## objetivo del terminal:

## 🔧 Funcionalidades Requeridas:
1. **balance_mes_actual** - Cálculo de balance del mes actual
2. **dashboard_mensual** - Resumen mensual con métricas clave
3. **gastos_por_entidad_y_concepto** - Agrupación de gastos
4. **harvest_stock** - Gestión de stock de cosechas
5. **retiros_por_socio** - Análisis de retiros por socio
6. **stock_actual** - Consulta de stock actualizado
7. **sum_expenses** - Sumatoria de gastos
8. **sum_withdrawals** - Sumatoria de retiros

## Estructura fisica :

```txt
[arca@alma-resist:~/trece/data]$ tree -l
.
├── management
│   ├── impositive
│   │   ├── boxes
│   │   │   └── boxes.csv            # id,name,entitie_id,inicial,alias,description,notes
│   │   └── movements
│   │       ├── expenses.csv         # id,date,amount,concept_id,entitie_id,caja_id,folio,description,notes
│   │       └── withdrawals.csv      # id,date,entitie_id,genetic_id,harvest_id,grams,price_id,status,paymethod_id,concept_id,notes,created_at
│   ├── people
│   │   └── entities.csv             # id,name,entities_type_id,tel,mail,notes
│   ├── settings
│   │   ├── concepts.csv             # id,name
│   │   ├── entities_types.csv       # id,name
│   │   ├── paymethods.csv           # id,name,
│   │   └── prices.csv               # id,name,amount
│   └── shed
│       ├── genetics
│       │   └── genetics.csv         # id,name,description,tag
│       ├── harvest
│       │   ├── harvest.csv          # id,harvest_id,genetic_id,grams
│       │   └── harvest_detail.csv   # id,cut_date,module_id,description,notes
│       └── modules
│           └── modules.csv          # id,name,description
└── README.md
```

Sugerencias: en withdrawals deberia calcular grams por el precio qe marca el price_id para calcular el precio total para los balances

## 🎯 Comandos Adicionales:
- `reload` - Recargar datos sin salir del terminal
- `help` - Sistema de ayuda integrado
- `exit`/`quit` - Salir del terminal

## 📋 Especificaciones Técnicas:
- Desarrollado en Python con módulo `cmd`
- Manejo robusto de errores
- Carga eficiente de datos CSV
- Formateo de salida claro y legible
- Persistencia de sesión hasta comando exit

**Por favor proporciona el código completo del terminal CLI con estas especificaciones.**


## changelog:
version: 0.1.1

