#!/bin/bash

# Navega a la carpeta donde está tu script base
cd /home/bird/Alma/alma_0.9.2/alma_0.9.2.0/00_ALMA_LIBRE/99_Sync/scripts/

# Mostrar todos los archivos .md disponibles
echo "📚 Archivos Markdown disponibles:"
find ../../ -name "*.md" | sort

# Separador visual
echo "-------------------------------------------"

# Ejecuta el script base para leer uno de esos archivos
python3 script_base.py
