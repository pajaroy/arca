#!/bin/bash

# Script para subir la carpeta Alma a Google Drive (remote 13CC)
# Autor: Santiago Calvo
# Fecha: 2025-05-08

echo "🔄 Iniciando sincronización de /home/bird/Alma a Google Drive (13CC:ALMA_BACKUP)..."

rclone sync /home/bird/Alma 13CC:ALMA_BACKUP --progress

echo "✅ Sincronización completada."