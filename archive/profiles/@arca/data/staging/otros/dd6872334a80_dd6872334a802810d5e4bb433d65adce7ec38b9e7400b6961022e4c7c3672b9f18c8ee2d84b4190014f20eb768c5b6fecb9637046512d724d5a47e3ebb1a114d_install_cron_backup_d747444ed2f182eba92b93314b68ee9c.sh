---
tipo: script
id: SCRIPT_2025-06-05_b77a8a
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Install Cron Backup
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:9f7a4cc6276eaef1a5173008ceda6b5d6d2cdf3cb93a64c8392159e00d008d48
---
#!/bin/bash

# Script para instalar el cron de backup automático cada 15 minutos

CRON_JOB="*/15 * * * * /home/bird/ALMA_RESIST/core/scripts/backup_to_git/backup_to_git.sh"
CRON_EXISTS=$(crontab -l 2>/dev/null | grep -F "$CRON_JOB")

if [ -z "$CRON_EXISTS" ]; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "[CRON] Tarea de backup instalada correctamente."
else
    echo "[CRON] La tarea de backup ya está configurada."
fi

# Al final de install_cron_backup.sh
touch ~/.backup_cron_installed
