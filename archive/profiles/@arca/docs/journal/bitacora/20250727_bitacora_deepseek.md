# BITÁCORA: CONSTRUCCIÓN DE BASE DE DATOS ALMA_RESIST

## FASE 1: ORGANIZACIÓN INICIAL (DÍA 1)
✔ **Objetivo**: Clasificar archivos caóticos en una estructura usable.
✔ **Acciones**:
  - Usamos `find` + `md5sum` para mover archivos a carpetas por tipo (.md, .yaml, .log, etc.).
  - Cada archivo se renombró con su hash para evitar duplicados.
  - Eliminamos directorios vacíos y archivos temporales.
✔ **Aprendizaje**:
  - Los hashes MD5 son útiles para identificar duplicados exactos.
  - `find -exec` es poderoso para operaciones masivas.

## FASE 2: EXTRACCIÓN DE METADATOS (DÍA 2)
✔ **Objetivo**: Crear una base de datos con información clave de los archivos.
✔ **Problema**: Algunos archivos tenían codificación corrupta (UTF-8 inválido).
✔ **Solución**:
  - Script Python con manejo robusto de errores:
    - Lectura en modo binario (`'rb'`).
    - Decodificación con `errors='replace'`.
    - Sanitización de textos con caracteres especiales.
✔ **Resultado**:
  - CSV limpio (`alma_resist_db.csv`) con:
    - Rutas, tipos, tamaños, fechas, palabras clave y hashes.
✔ **Aprendizaje**:
  - Siempre validar codificaciones en datos crudos.
  - Python es ideal para procesamiento complejo con errores.

## FASE 3: ANÁLISIS DE CONTENIDO (DÍA 3)
✔ **Objetivo**: Identificar temas clave para ALMA_RESIST.
✔ **Herramientas**:
  - Comandos UNIX (`grep`, `sort`, `uniq`) para conteos básicos.
  - Python + Pandas para análisis avanzado (opcional).
✔ **Descubrimientos**:
  - Tópicos recurrentes: "linux", "seguridad", "backup", "criptografía".
  - Archivos problemáticos: 15/10,000 con codificación rara (aislados).
✔ **Aprendizaje**:
  - Los archivos .md y .txt son la mayor fuente de conocimiento.
  - 80% de los archivos comparten patrones de tags.

## FASE 4: OPTIMIZACIÓN (DÍA 4)
✔ **Mejoras aplicadas**:
  - Backup de archivos originales en `/home/arca/archivo_backup/`.
  - Índices SQLite para búsquedas rápidas.
  - Documentación de estructura en `README_ALMA.md`.
✔ **Aprendizaje**:
  - SQLite es suficiente para bases de datos medianas (hasta 1TB).

## PRÓXIMOS PASOS
◼ **Integración con ALMA_RESIST**:
  - Usar el CSV/SQLite para construir un motor de búsqueda.
◼ **Automatización**:
  - Script que actualice la base diariamente con nuevos archivos.
◼ **Análisis avanzado**:
  - Clusterización de documentos por temas (NLP con spaCy).

## COMANDOS CLAVE APRENDIDOS
1. Buscar duplicados exactos:
   `find /ruta/ -type f -exec md5sum {} + | sort | uniq -d -w32`

2. Extraer palabras clave de textos:
   `grep -o -E '\w{4,}' archivo.txt | tr '[:upper:]' '[:lower:]' | sort | uniq -c`

3. Sanitizar codificación:
   `iconv -f utf-8 -t utf-8//IGNORE archivo_original -o archivo_limpio`

## ERRORES COMUNES Y SOLUCIONES
✖ **Problema**: "UnicodeDecodeError" en Python.
  ✓ **Solución**: Usar `open(..., 'rb').read().decode('utf-8', errors='replace')`.

✖ **Problema**: "Argument list too long" en `find`.
  ✓ **Solución**: Usar `-exec` o `xargs`.

## FASE 5: CLASIFICACIÓN SEMI-AUTOMÁTICA (DÍA 5)
✔ **Objetivo**: Transformar datos crudos en conocimiento estructurado.
✔ **Herramientas**:
  - Regex + Pandas para análisis de contexto.
  - grep + xargs para clasificación basada en reglas.
  - Graphviz para visualización de relaciones.
✔ **Resultados**:
  - 10 categorías principales identificadas.
  - Mapa visual de conexiones entre temas.
  - Índice de búsqueda instantánea con Recoll.
✔ **Lección clave**:
  - 20% de las palabras clave explican 80% del contenido (Principio de Pareto).