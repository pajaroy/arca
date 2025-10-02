---
type: "changelog"
date: "2025-08-21"
version: "0.2.0"
description: "changelog version 0.1.4 - 0.2.0"
linked_to: "'~/trece/archive/history/trece/src/cli/impositive/data_v0.2.0.py'"
---

# Terminal CLI Mejorado para Gestión de Planillas CSV - Versión 0.2.0

He optimizado el terminal CLI para adaptarlo a la nueva estructura de archivos y he implementado mejoras significativas en los cálculos y eficiencia. Aquí está el código completo:


## Script :


root = '~/trece/archive/history/trece/src/cli/impositive/data_v0.2.0.py'

## Mejoras implementadas en la versión 0.2.0:

1. **Carga de datos optimizada**: 
   - Ahora busca recursivamente en todos los subdirectorios de `data/`
   - Combina archivos con el mismo nombre en diferentes directorios
   - Construye índices para acelerar las búsquedas

2. **Funciones auxiliares para acceso a datos**:
   - `get_entity_name()`, `get_concept_name()`, `get_genetic_name()`, etc.
   - Eliminan código repetitivo y mejoran el rendimiento

3. **Manejo de errores robusto**:
   - Try-catch en cada procesamiento de registro
   - Continúa procesando incluso si hay registros corruptos

4. **Nuevos campos considerados**:
   - `concept_id` en retiros y gastos
   - `status` en retiros para filtrar por estado
   - `caja_id` en gastos para tracking de cajas

5. **Nuevos comandos**:
   - `estado_cajas` para mostrar el estado de las cajas

6. **Mejoras en visualización**:
   - Formateo de tablas más legible
   - Porcentajes en dashboard
   - Opciones de filtrado en comandos

7. **Optimizaciones de rendimiento**:
   - Uso de índices para búsquedas rápidas
   - Reduce la complejidad algorítmica de las operaciones

Este código está listo para usar con la nueva estructura de directorios y aprovecha todos los nuevos campos disponibles en los CSV.
