#!/bin/bash

# Script maestro para sincronizar carpetas a Google Drive con rclone
# Autor: Santiago Calvo
# Fecha: 2025-05-08

echo "🌀 Sincronización de Google Drive – Sistema ALMA"
echo "Seleccione una opción:"
echo "1) Subir carpeta completa Alma → ALMA_BACKUP (Drive personal)"
echo "2) Subir solo 13_CANNABIS_CLUB → carpeta compartida en Drive"
echo "3) Subir ambas"
echo "4) Cancelar"
read -p "Opción: " opcion

case $opcion in
  1)
    echo "🔄 Subiendo /home/bird/Alma → 13CC:ALMA_BACKUP ..."
    rclone sync /home/bird/Alma 13CC:ALMA_BACKUP --progress
    echo "✅ Backup completo sincronizado."
    ;;
  2)
    echo "🔄 Subiendo /home/bird/Alma/13_CANNABIS_CLUB → 13CC:13_CANNABIS_CLUB ..."
    rclone sync /home/bird/Alma/13_CANNABIS_CLUB 13CC:13_CANNABIS_CLUB --progress
    echo "✅ Carpeta 13CC sincronizada."
    ;;
  3)
    echo "🔄 Subiendo ambas carpetas..."
    rclone sync /home/bird/Alma 13CC:ALMA_BACKUP --progress
    rclone sync /home/bird/Alma/13_CANNABIS_CLUB 13CC:13_CANNABIS_CLUB --progress
    echo "✅ Ambas carpetas sincronizadas correctamente."
    ;;
  4)
    echo "❌ Cancelado por el usuario."
    ;;
  *)
    echo "⚠️ Opción inválida. Intente de nuevo."
    ;;
esac