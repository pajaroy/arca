---
tipo: script
id: SCRIPT_2025-06-05_4c2229
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Compress Alma Resist
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:8ab1d7e9af5c97d920d93ca9cd0cc3605bf0e1ab510f80a62d704787909021d5
---
#!/bin/bash

# Ruta del zip final
OUTPUT="/home/bird/Alma/ALMA_RESIST/alma_resist_compressed.zip"

# Nos movemos al root del proyecto
cd /home/bird/Alma/ALMA_RESIST || exit 1

# Creamos el zip solamente con los archivos que no estén ignorados por Git
git ls-files > /tmp/files_to_zip.txt

# Comprimimos
zip -r "$OUTPUT" -@ < /tmp/files_to_zip.txt

echo "✅ Proyecto comprimido correctamente en: $OUTPUT"

