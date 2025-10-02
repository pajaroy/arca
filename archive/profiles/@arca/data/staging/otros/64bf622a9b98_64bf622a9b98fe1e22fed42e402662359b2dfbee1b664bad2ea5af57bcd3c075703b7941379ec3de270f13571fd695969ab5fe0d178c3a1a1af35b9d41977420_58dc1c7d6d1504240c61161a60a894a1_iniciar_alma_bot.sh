#!/bin/bash

# ALMA LIBRE v0.3 – Lanzador del buffer_bot con IA local

export TELEGRAM_TOKEN="7666744025:AAFo3iiw9loASRl5AyaDK7zqr-HUnwTxwLQ"
export CHAT_ID="-1002137292219"
export LLM_ENDPOINT="http://localhost:5000/v1/completions"

cd "$(dirname "$0")"
echo "🚀 Iniciando ALMA LIBRE v0.3 – buffer_bot.py"
python3 buffer_bot.py
