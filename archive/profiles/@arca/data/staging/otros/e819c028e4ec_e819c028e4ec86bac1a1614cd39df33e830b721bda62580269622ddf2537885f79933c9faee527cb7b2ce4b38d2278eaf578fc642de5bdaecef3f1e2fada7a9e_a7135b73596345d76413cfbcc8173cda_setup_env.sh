#!/bin/bash

echo "🌱 Creando entorno virtual..."
python3 -m venv env_alma

echo "✅ Entorno creado. Activando..."
source env_alma/bin/activate

echo "📦 Instalando dependencias..."
pip install click

echo "🎉 Entorno listo. Ya podés correr memoria_loader.py"
