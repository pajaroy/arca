---
tipo: script
id: SCRIPT_2025-06-05_f36691
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Alma Autostart Tmux
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:c9f79b77db149628a23eef9b95fe6b42a82a12d449b6c9d85a61e95790d0ddb4
---
#!/bin/bash

SESSION="alma_boot"

# Comprobar si ya está corriendo la sesión
tmux has-session -t $SESSION 2>/dev/null
if [ $? != 0 ]; then
    # Crear nueva sesión en segundo plano
    tmux new-session -d -s $SESSION

    # Ventana 1: iniciar servidor SSH si no está activo
    tmux rename-window -t $SESSION:0 'ssh-server'
    tmux send-keys -t $SESSION 'sudo systemctl start ssh' C-m

    # Ventana 2: iniciar Input Leap (servidor)
    tmux new-window -t $SESSION -n 'input-leap'
    tmux send-keys -t $SESSION 'input-leaps --no-tray --disable-crypto --name alma-core --config ~/.input-leap/input-leap.conf' C-m

    # Ventana 3: sincronizar carpeta ALMA_RESIST (hacia la otra máquina)
    tmux new-window -t $SESSION -n 'sync-to-resist'
    tmux send-keys -t $SESSION 'rsync -avz --delete --exclude-from=/home/bird/ALMA_RESIST/.rsync_exclude /home/bird/ALMA_RESIST/ bird@192.168.1.36:/home/bird/ALMA_RESIST/' C-m
fi
