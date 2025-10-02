#!/bin/bash

# === ALMA LIBRE v0.2 – Lanzador del buffer_bot ===

# Exportar variables de entorno
export TELEGRAM_TOKEN="7666744025:AAFo3iiw9loASRl5AyaDK7zqr-HUnwTxwLQ"
export CHAT_ID="-1002137292219"

# Navegar al directorio del bot (ajustá si cambia)
cd "$(dirname "$0")"

# Ejecutar el bot
echo "🚀 Iniciando ALMA LIBRE v0.2 – buffer_bot.py"
python3 buffer_bot.py
