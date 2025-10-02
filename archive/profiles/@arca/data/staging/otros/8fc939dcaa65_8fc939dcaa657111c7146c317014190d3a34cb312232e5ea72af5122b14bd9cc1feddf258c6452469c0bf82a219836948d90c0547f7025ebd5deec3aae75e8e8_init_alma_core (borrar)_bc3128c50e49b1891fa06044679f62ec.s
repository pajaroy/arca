---
tipo: script
id: SCRIPT_2025-06-05_50f585
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Init Alma Core (Borrar)
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:1ebad311df85674014efaf51ea25059071655bcf0a63038104ca01bb84308810
---
#!/bin/bash

# Iniciar Syncthing si no está corriendo
pgrep syncthing > /dev/null || syncthing &

# Iniciar Input Leap si no está corriendo
pgrep input-leap > /dev/null || input-leap &

# Iniciar backup_to_git si no está corriendo
pgrep -f backup_to_git.sh > /dev/null || nohup /home/bird/ALMA_RESIST/core/scripts/backup_to_git/backup_to_git.sh > /dev/null 2>&1 &
