#!/bin/bash
# ~/@arca/source/main.py
# Descripcion: Script para clasificar archivos por formato
#  - Extrae archivos de cualquier carpeta
#  - Calcula el hash con blake3
#  - Verifica los hash en destino para evitar colisiones
#  - Revisa con fdupes (o alguna alternativa para evitar duplicados textuales)
#  - Genera logs de cada archivo
#
#
#
#
# Estructura: 
#
#
##################################################################################

import os
import blake3
import shutil

# Ruta base:
# Esto podriamos definirlo como rutas relativas al path base , pero bueno lo iremos mejorando poco a poco 
root_base="~/@arca"
root_source="~/@arca/source"

# Crear directorios si no existe:

tipos=["csv","markdown","otros","python","sql","yaml"]

for dir in tipos:

    root_dir=os.path.join(root_source,dir)

    if not os.path.exists