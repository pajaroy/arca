#!/bin/bash

echo "🔧 Iniciando integración de nuevo archivo..."

# Activar entorno virtual si existe
if [ -f "venv/bin/activate" ]; then
  echo "🐍 Activando entorno virtual"
  source venv/bin/activate
  VENV_ACTIVATED=true
else
  echo "⚠️ Entorno virtual 'venv' no encontrado, se asume entorno ya activo"
  VENV_ACTIVATED=false
fi

echo "🔍 Validando estructura con validate_docs.py"
python3 scripts/validate_docs.py ./docs

echo "🐍 Normalizando módulos a snake_case con force_snake_case_modules.py"
python3 scripts/force_snake_case_modules.py --root ./docs --backup --verbose

echo "🛠 Corrigiendo metadatos con fix_metadata.py"
python3 scripts/fix_metadata.py --root ./docs --backup --verbose

echo "✅ Validación final con validate_docs.py"
python3 scripts/validate_docs.py ./docs

# Desactivar entorno solo si lo activamos en este script
if [ "$VENV_ACTIVATED" = true ]; then
  echo "🧹 Desactivando entorno virtual"
  deactivate
fi

echo "🎉 Proceso completado exitosamente"
