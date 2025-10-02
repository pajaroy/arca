---
tipo: script
id: SCRIPT_2025-06-05_b7f426
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Init Alma Core
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:8f7dd82db13ae2029e0aa63d7bdb888ecaf1e227c2c795af59073af1d5006ad4
---
#!/bin/bash

# === Sistema de Inicialización ALMA_CORE ===
# Versión: 2025-06-02
# Nodo: alma-core
# Ubicación: /home/bird/ALMA_RESIST/core/scripts/init_system/init_alma_core.sh

echo "[INIT] Iniciando entorno ALMA_CORE..."

# === Validar hostname ===
HOSTNAME=$(hostname)
if [ "$HOSTNAME" != "alma-core" ]; then
  echo "[INIT] Este script solo debe ejecutarse en alma-core. Abortando."
  exit 1
fi

# === Iniciar Syncthing si no está corriendo ===
pgrep syncthing > /dev/null || syncthing &

# === Iniciar Input Leap si no está corriendo ===
pgrep input-leap > /dev/null || input-leap &

# === Iniciar backup_to_git si no está corriendo ===
pgrep -f backup_to_git.sh > /dev/null || nohup /home/bird/ALMA_RESIST/core/scripts/backup_to_git/backup_to_git.sh > /dev/null 2>&1 &

# === Validar clave SSH cargada ===
if ! ssh-add -l | grep -q "ED25519"; then
  echo "[INIT] Clave SSH no detectada, intentando cargar..."
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_ed25519
fi

# === Iniciar Obsidian apuntando a ALMA_RESIST ===
pgrep Obsidian > /dev/null || (nohup /home/bird/apps/Obsidian.AppImage ~/ALMA_RESIST > /dev/null 2>&1 &)

# === Iniciar VSCode apuntando a ALMA_RESIST ===
pgrep code > /dev/null || (nohup code ~/ALMA_RESIST > /dev/null 2>&1 &)

echo "[INIT] Entorno ALMA_CORE inicializado correctamente."


