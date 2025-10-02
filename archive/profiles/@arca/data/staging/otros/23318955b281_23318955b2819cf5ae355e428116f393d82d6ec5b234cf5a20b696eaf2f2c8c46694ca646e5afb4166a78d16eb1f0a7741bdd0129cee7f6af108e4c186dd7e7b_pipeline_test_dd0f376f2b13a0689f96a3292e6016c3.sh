#!/bin/bash

# Ruta al script CLI
CLI="python3 alma_cli_cleaner.py"
ARCHIVO="test.md"
RESPONSABLE="Bird"
LINKED="relacionado1.md,relacionado2.md"

# 1. CREAR el archivo con metadatos iniciales
$CLI crear "$ARCHIVO" --title "Archivo Test" --responsable "$RESPONSABLE" --linked-to "$LINKED"
if [ $? -ne 0 ]; then
  echo "❌ Error en 'crear'"
  exit 1
fi

# 2. VALIDAR el archivo
$CLI validar "$ARCHIVO"
if [ $? -ne 0 ]; then
  echo "❌ Error en 'validar'"
  exit 1
fi

# 3. LIMPIAR el archivo (opcional, normalmente después de editarlo)
$CLI limpiar "$ARCHIVO"
if [ $? -ne 0 ]; then
  echo "❌ Error en 'limpiar'"
  exit 1
fi

# 4. Cambiar RESPONSABLE
$CLI set_responsable "$ARCHIVO" --responsable "Bird,Kael"
if [ $? -ne 0 ]; then
  echo "❌ Error en 'set_responsable'"
  exit 1
fi

# 5. Vincular a más archivos (LINKED)
$CLI set_linked "$ARCHIVO" --linked-to "otro_relacionado.md"
if [ $? -ne 0 ]; then
  echo "❌ Error en 'set_linked'"
  exit 1
fi

# 6. Mostrar LOG/HISTORIAL
$CLI log "$ARCHIVO"
if [ $? -ne 0 ]; then
  echo "❌ Error en 'log'"
  exit 1
fi

echo "✅ Pipeline de comandos ejecutado exitosamente sobre $ARCHIVO"
