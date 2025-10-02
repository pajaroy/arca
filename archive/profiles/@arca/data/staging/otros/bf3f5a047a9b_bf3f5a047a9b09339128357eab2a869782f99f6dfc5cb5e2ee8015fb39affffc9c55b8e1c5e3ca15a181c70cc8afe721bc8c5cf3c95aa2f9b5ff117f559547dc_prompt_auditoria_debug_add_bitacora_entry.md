# Prompt – Auditoría y Debugging de Script `add_bitacora_entry.py` (Bitácora Viva ALMA_RESIST)

**Contexto:**  
Estamos auditando el script CLI `add_bitacora_entry.py`, encargado de agregar entradas a la bitácora viva institucional en formato YAML, conforme a la especificación `IDEA_BASE_BITACORA_SCRIPT_2025-06-06_01`.  
Se detectó que, a pesar de no arrojar errores, el script no agrega efectivamente nuevas entradas al archivo de destino (`bitacora_viva.yaml`). Se requiere identificar el motivo real (sea bug de lógica, formato, permisos o ruta) y dejar la investigación documentada.

**Pasos realizados:**
- Se creó backup de la bitácora antes de cada prueba.
- Se vació el archivo de bitácora a `entradas: []`.
- Se ejecutó el script con distintos argumentos y rutas.
- Se verificó que el mensaje “Entrada agregada exitosamente a la bitácora” aparezca.
- Se inspeccionó el archivo YAML antes y después de cada ejecución.
- Se recomendó agregar prints de debugging en cada paso crítico del script (carga, append, guardado).

**Objetivo del prompt:**  
Solicitar un análisis crítico del flujo de ejecución, posibles puntos de fallo, sugerencias de debugging, y una versión “instrumentada” (con prints) del script para aislar el bug.

---

### **INSTRUCCIONES**
- Auditá el script y explicá qué puntos podrían estar impidiendo el guardado.
- Proponé pruebas manuales mínimas para aislar el error.
- Si es posible, devolvé una versión del script que incluya prints de debugging tras cada función clave.
- Listá buenas prácticas para asegurar trazabilidad y seguridad en scripts de automatización documental.
- Dejá todo en formato legible para archivar como “bitácora viva” y changelog.

---

## **Bitácora viva – Proceso de debugging y aseguramiento de script bitácora**

```yaml
entradas:
  - fecha: 2025-06-06
    accion: "Debugging y auditoría script bitácora"
    descripcion: |
      - Se identificó que el script `add_bitacora_entry.py` no agregaba entradas, a pesar de ejecutarse sin errores ni advertencias.
      - Se revisaron posibles causas: permisos, rutas, estructura YAML, encoding y flujo lógico.
      - Se instrumentó el script con prints para ver cada paso de ejecución.
      - Se validó la estructura previa del archivo y su timestamp antes y después de cada prueba.
      - Se dejó registro completo de pasos y backups en bitácora para trazabilidad total.
    motivo: "Aseguramiento de integridad y funcionamiento antes de automatizar la bitácora institucional."
    ejecutado_por: "Santi & Kael"
    estado: "En debugging"
    tags:
      - debug
      - bitacora
      - auditoria
      - backup
      - mvp
