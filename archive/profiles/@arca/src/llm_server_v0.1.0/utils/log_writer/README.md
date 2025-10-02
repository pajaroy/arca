---
id: log_writer_llm_server_v0.2
modulo: log_writer
version: 0.2
standard: ALMA_RESIST_v0.2
descripcion: |
  Backend avanzado de escritura y rotación de logs estructurados.
  Gestiona compresión, cifrado (integrado con log_crypto) y permite hooks para rotación diaria/por módulo.
  Soporta futura consulta CLI de logs históricos.
campos_universales:
  - id
  - agente
  - timestamp
  - tags
  - hash
  - metadata
scripts_principales:
  - log_writer.py: "Escribe, rota y prepara logs para cifrado/consulta"
dependencias:
  - logging_config
  - log_crypto
ejemplo_uso: |
  from log_writer import rotate_logs, write_log
  rotate_logs("modulo_x")
linked_to:
  - alma_core/control_central/bitacora/bitacora_viva.yaml
estado: "EN USO — rotación y cifrado institucional"

---

