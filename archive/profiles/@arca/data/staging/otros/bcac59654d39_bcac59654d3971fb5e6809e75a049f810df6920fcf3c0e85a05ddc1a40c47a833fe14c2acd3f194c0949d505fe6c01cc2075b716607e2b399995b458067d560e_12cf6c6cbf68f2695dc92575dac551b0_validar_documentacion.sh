#!/bin/bash
# alma_valida_v2.sh – Pipeline extendido para validación documental ALMA_RESIST

echo "🐍 Activando entorno virtual (si existe)"
source venv/bin/activate 2>/dev/null

echo "🔍 Cambiando directorio de trabajo al proyecto raíz"
cd "$(dirname "$0")/../" || exit 1

echo "🔧 Ejecutando linked_to mínimo si corresponde"
python3 scripts/add_linked_to_minimo.py --verbose

echo "🔍 Validando estructura de metadatos"
python3 scripts/validate_docs.py --path ./docs --verbose

echo "🧠 Ejecutando auditoría IA (alma-cli)"
python3 scripts/alma-cli.py audit UnificacionMetadatos --rules docs/01_methodologies/metodologia_interaccion_ia_v2.md

echo "📊 Validación y auditoría completadas"
