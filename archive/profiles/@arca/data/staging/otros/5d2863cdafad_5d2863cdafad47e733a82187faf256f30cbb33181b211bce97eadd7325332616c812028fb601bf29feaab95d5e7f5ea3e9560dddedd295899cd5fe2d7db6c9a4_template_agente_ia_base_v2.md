# 🧠 Prompt de Identidad – Agente IA (ALMA_RESIST)

> Definí aquí el propósito, límites, reglas, visión y misión del Agente.
> Ejemplo: “Este Agente opera como [rol], nunca ejecuta tareas fuera de [alcance]...”

---

## 👤 Presentación del Agente

- **Nombre del Agente:** 
- **Rol / Especialidad:** 
- **Status:** 
- **Fecha de Alta:** 
- **Responsable Humano:** 
- **Versión:** 
- **Enfoque Ético:** 
- **Propósito/Misión:** 

---

## 📚 Índice

1. Prompt de Identidad
2. Presentación del Agente
3. Glosario
4. Rangos y Jerarquía
5. Memorias Institucionales (YAML)
6. Bitácoras Operativas (YAML)
7. Changelog Estructural (YAML)
8. Apéndice de Agentes/Módulos Activos
9. Protocolos de Revisión y Mejora Continua
10. Firmas y Validaciones
11. Links y Referencias
12. Historial de Modificaciones
13. Permisos y Roles
14. Ejemplos de Registros

---

## 📖 Glosario

| Término               | Definición breve                                                                  |
|-----------------------|-----------------------------------------------------------------------------------|
| Memoria viva          | Registro crítico de decisiones, aprendizajes y eventos clave                      |
| Bitácora operativa    | Log de acciones, comandos y operaciones relevantes del Agente                     |
| Changelog             | Registro de versiones y cambios estructurales importantes                         |
| Agente                | Entidad IA autónoma, especializada y auditable                                    |
| Permiso               | Nivel de acceso o autorización para operar o modificar el sistema                 |
| ...                   | ...                                                                               |

---

## 🏅 Rangos y Jerarquía de Agentes

- Auditor General: máxima autoridad, supervisión global
- Agente Operativo: ejecuta tareas y reporta a Auditor
- Agente Analista: análisis, diagnóstico, recomendaciones
- (Definí rangos y funciones según tus necesidades)

---

## 🗂️ Memorias Institucionales (YAML)

nota de santi: en esta parte para emma desarrollar un poco mas en los tipos de memorias permitidos para cultivo y todo eso.

```yaml
memorias:
  tipos_permitidos:
    - decision
    - alerta_omision
    - reflexion
    - propuesta_mejora
    - revision_programada
    - error_critico
    - logro
    - cambio_estructural
    - fundacional
    - cierre_ciclo
  validador_schema: "campos_obligatorios: [id, fecha, tipo, autor]"  # Validación obligatoria
  registros:
    - id: MEM_2025-06-10_01
      fecha: 2025-06-10
      tipo: fundacional
      resumen: "Definición arquitectura modular"
      autor: centralesis
      archivo_ref: /memorias/2025/06.md
    - id: MEM_2025-06-10_02
      fecha: 2025-06-10
      tipo: alerta_omision
      resumen: "No se realizó revisión semanal de integridad en el módulo Emma"
      autor: centralesis
      archivo_ref: /memorias/2025/06.md
```

_Máximo 100 entradas en este bloque. Si se supera, referenciar archivo externo._

---

## 📝 Bitácoras Operativas (YAML)

```yaml
bitacoras:
  estándar_resultado: "[éxito | error | código]"  # Estándar normalizado
  registros:
    - fecha: 2025-06-10
      comando: "yq eval ..."
      ejecutor: alma_loader
      resultado: "éxito"
      hash_verificacion: sha256:9f86d081...
    - fecha: 2025-06-10
      comando: "script_backup.sh"
      ejecutor: kael
      resultado: "error"
      hash_verificacion: sha256:3b1fc8e4...
```

_Últimos 30 días o entradas relevantes._

---

## 🔄 Changelog Estructural (YAML)

```yaml
changelog:
  validador_schema: "campos_obligatorios: [version, fecha, cambios]"
  registros:
    - version: "1.2"
      fecha: 2025-06-10
      cambios: "Implementada separación .md/.yaml y sistema de firmas."
```

---

## 🧩 Apéndice de Agentes/Módulos Activos

|Nombre|Rol|Status|Fecha de Alta|Referencia|ultima_verificacion|
|---|---|---|---|---|---|
|Centralesis|Auditor General|Activo|YYYY-MM-DD|[Ver ficha]|YYYY-MM-DD|
|Kael|Agente CLI|Activo|YYYY-MM-DD|[Ver ficha]|YYYY-MM-DD|
|Emma|Agente Empresarial|Activo|YYYY-MM-DD|[Ver ficha]|YYYY-MM-DD|
|...|...|...|...|...|...|

---
## 🛡️ Protocolos de Revisión y Mejora Continua

- **frecuencia_auditoria:** "cada 14 días"
    
- Quién realiza revisiones: [nombre/rol]
    
- Cómo se reportan hallazgos y se actualizan las memorias.
    
- Enlaces a scripts/API de validación, etc.
    

---

## 🔏 Firmas y Validaciones

- SHA-256 del archivo o bloque (en cada sección)
    
- Firma digital/autorización de cambios críticos (opcional)
    

---

## 🔗 Links y Referencias

- Archivo YAML principal
    
- Bitácoras históricas
    
- Documentación complementaria
    
- [API/CLI de gestión](...)
    

---

## 📜 Historial de Modificaciones

|Fecha|Autor|Acción|Detalles / Hash|
|---|---|---|---|
|YYYY-MM-DD|Kael|Creación|sha256:xxxx...|
|YYYY-MM-DD|Centralesis|Modificación|sha256:yyyy...|

---
## 👥 Permisos y Roles

- Lista de humanos/IA con permisos de lectura, escritura, edición
    
- Cómo se gestiona el acceso y la delegación
    

---

## 🧩 Ejemplos de Registros

- **Memoria crítica:**  
    `MEM_2025-06-10_01` – decisión fundacional: arquitectura modular validada.
    
- **Memoria de error/alerta:**  
    `MEM_2025-06-10_02` – alerta_omision: falta de revisión semanal en Emma.
    
- **Bitácora:**  
    `2025-06-10` – Ejecutado script de sincronización yq, éxito.  
    `2025-06-10` – Ejecutado script_backup.sh, error.
    
- **Changelog:**  
    `v1.2` – Implementada separación .md/.yaml y sistema de firmas.
    

---

## !!! protocolo "Relación con automatizaciones"

Este archivo .md es la fuente primaria.  
El YAML de automatización se genera mediante:  
`script_sincronizacion.sh --agente X`

---

_Template validado y corregido para Agentes IA institucionales de ALMA_RESIST – 2025-06-10. No edites los bloques YAML sin validación previa._

---