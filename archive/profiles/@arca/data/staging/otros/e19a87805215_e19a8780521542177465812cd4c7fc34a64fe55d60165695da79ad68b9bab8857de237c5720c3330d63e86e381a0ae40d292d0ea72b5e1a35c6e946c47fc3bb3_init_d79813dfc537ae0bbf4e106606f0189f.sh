---
tipo: script
id: SCRIPT_2025-06-05_3a151e
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Init
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:9656f62b1ab867d0aabc2e457f4d7c7dbd3886fba668b69b0a2bf42277382ed5
---
#!/bin/bash

# === [ ALMA INIT SCRIPT ] ===

# Iniciar Syncthing si no est치 corriendo
pgrep syncthing > /dev/null || syncthing &

# Iniciar Input Leap si no est치 corriendo
pgrep input-leap > /dev/null || input-leap &

# Iniciar backup_to_git si no est치 corriendo
pgrep -f backup_to_git.sh > /dev/null || nohup /home/bird/ALMA_RESIST/core/scripts/backup_to_git/backup_to_git.sh > /dev/null 2>&1 &

# Iniciar Obsidian apuntando al vault ALMA_RESIST
pgrep Obsidian > /dev/null || (nohup /home/bird/apps/Obsidian.AppImage ~/ALMA_RESIST > /dev/null 2>&1 &)

# Iniciar VSCode apuntando al proyecto ALMA_RESIST
pgrep code > /dev/null || (nohup code ~/ALMA_RESIST > /dev/null 2>&1 &)

# Validar y activar agente SSH si es necesario
if ! pgrep -u "$USER" ssh-agent > /dev/null; then
    eval "$(ssh-agent -s)"
fi

# Cargar clave SSH si no est치 cargada
ssh-add -l | grep "id_ed25519" > /dev/null || ssh-add ~/.ssh/id_ed25519 2> /dev/null
