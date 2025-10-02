---
id: contracts_llm_server_v0.2
descripcion: |
  Carpeta de contratos y validadores JSON Schema del LLM Server.
  Define la estructura formal de los mensajes de entrada (prompt) y salida (respuesta) del endpoint principal /responder.
  La versión v0.2 extiende el contrato para soportar trazabilidad multiagente, referencia cruzada a memorias, integración con el CLI y gobernanza institucional.
version: 0.2
fecha_actualizacion: 2025-06-11
archivos_criticos:
  - schema_prompt.json
  - schema_respuesta.json
estado: "FUNCIONAL Y ALINEADO — Compatible con memoria única ALMA_RESIST"
compatibilidad:
  - main.py
  - transport_layer.py
  - cli multiagente ALMA_RESIST
campos_schema_prompt:
  - id: "Identificador único de la petición (opcional)"
  - agente: "Nombre del agente humano/IA que origina el prompt (obligatorio)"
  - prompt: "Texto enviado al modelo LLM (obligatorio)"
  - tags: "Temas o módulos asociados (opcional)"
  - contexto: "Contexto adicional o memoria relevante para el prompt (opcional)"
  - hash: "Hash de integridad del prompt (opcional)"
campos_schema_respuesta:
  - id: "Identificador correlativo con el prompt original (opcional)"
  - respuesta: "Texto generado por el modelo LLM (obligatorio)"
  - agente: "Nombre del agente que responde (opcional)"
  - tags: "Etiquetas asociadas a la respuesta (opcional)"
  - memoria_ref: "IDs de memorias institucionales referenciadas (opcional)"
  - hash: "Hash de integridad de la respuesta (opcional)"
  - metadata:
      - modelo: "Identificador del modelo"
      - longitud_prompt: "Largo del prompt original"
      - timestamp: "Marca de tiempo de la respuesta"
      - estado: "Estado de la respuesta (success, error, warning, etc.) (opcional)"
historial_cambios:
  - fecha: 2025-06-11
    version: 0.2
    resumen: >
      Se extendió el contrato base para permitir trazabilidad multiagente, referencia cruzada a memorias institucionales, y control de integridad con hashes. Compatible con CLI multiagente y memoria unificada.
  - fecha: 2025-06-08
    version: 0.1
    resumen: >
      Versión inicial. Solo campos prompt/respuesta y metadata básica. Sin soporte multiagente ni referencia a memoria.
mejoras_pendientes:
  - Integración dinámica de campos adicionales según necesidades futuras del ecosistema ALMA_RESIST.
  - Generar changelog y registrar toda actualización en bitácora crítica institucional.
linked_to:
  - /alma_core/core/notebooks/llm_server_v0.1.0/main.py
  - /alma_core/control_central/memorias/memoria_centralizada.yaml
  - /alma_core/core/notebooks/llm_server_v0.1.0/cli/
  - /alma_core/control_central/bitacora/bitacora_viva.yaml
notas: |
  Toda modificación de los contratos debe registrarse en el changelog institucional y ser validada por auditoría.
  La trazabilidad y compatibilidad hacia atrás deben ser prioridad en futuros cambios.

---

