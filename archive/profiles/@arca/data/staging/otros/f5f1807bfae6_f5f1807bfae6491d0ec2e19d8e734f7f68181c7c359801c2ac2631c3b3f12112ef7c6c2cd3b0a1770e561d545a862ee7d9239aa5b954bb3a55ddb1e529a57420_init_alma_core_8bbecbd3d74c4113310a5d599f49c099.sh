#!/bin/bash

# Iniciar Syncthing si no está corriendo
pgrep syncthing > /dev/null || syncthing &

# Iniciar Input Leap si no está corriendo
pgrep input-leap > /dev/null || input-leap &

# Iniciar backup_to_git si no está corriendo
pgrep -f backup_to_git.sh > /dev/null || nohup /home/bird/ALMA_RESIST/core/scripts/backup_to_git/backup_to_git.sh > /dev/null 2>&1 &

# Solo abrir Obsidian y VSCode si estamos en el nodo alma-resist
if [ "$(hostname)" = "alma-resist" ]; then
  pgrep Obsidian > /dev/null || (nohup /home/bird/apps/Obsidian.AppImage ~/ALMA_RESIST > /dev/null 2>&1 &)
  pgrep code > /dev/null || (nohup code ~/ALMA_RESIST > /dev/null 2>&1 &)
fi
