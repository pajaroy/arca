---
id: integration_context_tracker_v0.2
modulo: context_tracker
version: 0.2
standard: ALMA_RESIST_v0.2
descripcion: |
  Módulo para registrar, consultar y auditar interacciones prompt–respuesta en el ecosistema ALMA_RESIST.
  Permite tracking multiagente y referencia cruzada a memorias institucionales.
script_principal: context_tracker.py
campos_universales:
  - id
  - agente
  - timestamp
  - tags
  - hash
  - metadata
  - memoria_ref
funcion: |
  - Añade registros de interacción de forma validada y con hash automático.
  - Permite consultas filtradas por agente, tags, fecha, etc.
  - Prepara el contexto para motores RAG y agentes autónomos.
mejoras_pendientes:
  - Integración directa con CLI multiagente.
  - Exportación y paginación avanzada.
linked_to:
  - ../schemas/schemas.py
  - ../../../../control_central/bitacora/bitacora_viva.yaml
estado: "FUNCIONAL, alineado a la arquitectura universal."

---

