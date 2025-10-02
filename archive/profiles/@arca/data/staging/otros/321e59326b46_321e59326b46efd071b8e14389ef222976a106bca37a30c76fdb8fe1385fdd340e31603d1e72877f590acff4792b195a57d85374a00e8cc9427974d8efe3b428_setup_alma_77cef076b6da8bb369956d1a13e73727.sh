---
tipo: script
id: SCRIPT_2025-06-05_5dca68
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Setup Alma
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:aa454ea5b0483380cf03da4a58c89e9aef69c1ad66672fcb40923ec414d6596f
---
#!/bin/bash

# Ruta absoluta base del script (ajusta si cambiás la ubicación)
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../.." && pwd )"

echo "📦 Instalando dependencias del sistema (requiere sudo)..."
sudo apt update
sudo apt install -y python3 python3-pip tmux git nano

echo "🗃️ Instalando dependencias Python en entorno global..."
python3 -m pip install --upgrade pip

echo "🚀 Instalando requirements desde:"
echo "$BASE_DIR/requirements.txt"
pip install -r "$BASE_DIR/requirements.txt"

echo ""
echo "🎉 ALMA_RESIST listo para usar en este sistema."
echo "   - Python, tmux y dependencias instaladas."
echo "   - Para ejecutar tu proyecto:"
echo ""
echo "     cd $BASE_DIR"
echo "     source venv/bin/activate  # Si usás entorno virtual"
echo "     python core/alma.py       # O el script principal que uses"
echo ""
echo "   (Recordá montar tu pendrive si lo corrés externo)"
