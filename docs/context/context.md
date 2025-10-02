---
date: "2025-09-21"
name: "context_arca"
type: "context"
version: "0.1.0"
description: "Sistema personal de gestion de archivos"
linked_to: [/arca]
---
# Proyecto Arca – Contexto

**Arca** es el núcleo de un sistema personal de gestión y organización de archivos.  
La idea es que **arca** funcione como la “trinchera” o punto de entrada desde el cual se organiza, procesa y explora todo lo demás.

## Estructura actual
- `arca/` → Carpeta raíz principal del proyecto.
  - `src/` → Código fuente (scripts utilitarios, pruebas, procesadores).
  - `alma/`, `trece/`, etc. → Subcarpetas que actúan como espacios temáticos o de trabajo (archivos, backups, proyectos).
  - `archive/` → Archivos antiguos, respaldos, material guardado.

## Objetivo
1. Centralizar en **arca** todo el material (scripts, archivos, backups, metadatos).
2. Usar **arca/src** como punto de partida para herramientas de búsqueda, análisis y automatización.
3. Mantener la estructura flexible: se pueden anidar más carpetas internas (ejemplo: `arca/alma/src`) sin romper el flujo general.

## Estado actual
- Arca funciona como **gestor de archivos base**.
- Todavía no está montado sobre Docker ni automatizado por completo.
- Se están preparando scripts y configuraciones para:
  - Indexar y clasificar archivos.
  - Analizar metadatos.
  - Integrar con herramientas (Bash, Python, futuras bases de datos).

## Filosofía
- **Arca** es la base: todo depende de ella.
- Subcarpetas como `alma` o `trece` son extensiones/espacios de trabajo que igual dependen de la raíz `arca/`.
- Más adelante se piensa en expandir hacia contenedores y agentes autónomos, pero siempre con arca como centro.

---
