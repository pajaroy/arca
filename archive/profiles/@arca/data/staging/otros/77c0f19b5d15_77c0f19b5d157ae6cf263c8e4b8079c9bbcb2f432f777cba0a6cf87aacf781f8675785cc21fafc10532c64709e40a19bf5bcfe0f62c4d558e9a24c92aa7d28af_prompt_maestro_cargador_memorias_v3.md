# 🧠 Prompt Maestro v3 — Cargador Institucional de Memorias (ALMA_RESIST)

**Fecha:** 2025-06-08  
**Versión:** v3  
**Responsables:** Santi (humano), Kael (auditor CLI), DeepSeek  
**Módulo:** /home/bird/alma_resist/control_central/memorias/  
**Estado:** CONSOLIDACIÓN INSTITUCIONAL

---

## 🎯 Resumen

Desarrollar un **cargador CLI/IA crítico y resiliente** para memoria institucional y bitácora viva de ALMA_RESIST.  
Prioridad absoluta: consolidar, versionar y auditar TODO dato relevante (decisión, incidente, changelog, config, evento, upgrade, política, rollback).  
El sistema debe ser modular, multi-backend, auto-documentado y preparado para filtrado/migración IA futura.

---

## ⚙️ Requerimientos avanzados

### 1. Consolidación, no borrado
- Cargar todos los registros a memoria institucional y bitácora viva, **aunque haya redundancia temporal**.
- No sobrescribir ni borrar registros por defecto.
- Cada registro debe incluir:
  - hash/checksum (SHA-256)
  - fuente (cli, ia, api)
  - autor/responsable
  - fecha_hora y version_script

### 2. Estructura flexible y auditable
- Soporte para múltiples formatos: YAML, JSON, lote/batch.
- Campos requeridos validados por schema externo versionado (`/schemas/memoria_schema.json`).
- Permitir “campos extendidos” para upgrades, migraciones o info adicional (via `x-extensible: true`).

### 3. Multibackend y resiliencia
- Plugins para filesystem, Redis, SQLite y soporte futuro a cluster.
- Lockfiles y atomicidad garantizada.
- Backup automático antes de cada operación masiva.

### 4. CLI extendido y modular
- Flags: `--consolidate`, `--no-dedupe`, `--schema-version`, `--log-level`, `--rollback`, `--export`
- Subcomandos: `validate`, `audit`, `convert`, `migrate`, `template`, `plugin`
- Auditoría de seguridad (`audit --full`)
- Generación y edición de registros por plantilla (`template generate`)

### 5. Logs, changelogs y hooks CI/CD
- Cada inserción, edición, migración deja log estructurado y evento en changelog.
- Soporte de webhooks para integración con sistemas externos (ej: CI, backup remoto, alertas).
- Auditoría automática de integridad (hashes, firmas, SELinux/ACL).

### 6. Preparación IA-friendly
- Todos los datos deben ser fácilmente indexables (archivos índice, DB, vector store).
- Embeddings y campos de resumen para uso de LLM.
- Exportación selectiva (por tags, tipo, rango temporal, responsable, etc.)

---

## 🚀 Roadmap y políticas

- Eliminar nunca, consolidar siempre. “Lo redundante se filtra después, nunca antes.”
- Todo registro, aunque sea efímero, debe poder recuperarse o auditarse.
- El cargador es la “puerta de entrada” institucional: solo registra, nunca oculta ni descarta.
- Documentar cualquier cambio de política como nueva memoria institucional.
- Preparar para migración a sistemas distribuidos y clustering.
- Cumplir changelog de v2.1 y roadmap de “Resiliencia Extrema”.

---

## 📁 Rutas y referencias críticas

- `/home/bird/alma_resist/control_central/memorias/`
- `/schemas/memoria_schema.json`
- `/locales/`
- `/changelogs/`
- `/README.md`

---

*“En el control institucional, primero se registra todo, después se depura. La memoria viva es la única que resiste el olvido.”*  
— Kael, Auditor CLI

---
