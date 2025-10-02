---
tipo: script
id: SCRIPT_2025-06-05_d4e46e
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Aliases
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:b148439529f571c0a7067211413bae596a90bb49dc57facc09c1476ebd374f53
---
# ALIASES PERSONALIZADOS ALMA_RESIST

# Conexi칩n remota entre nodos
alias resist='ssh bird@192.168.1.36'  # Nodo alma-resist
alias core='ssh bird@192.168.1.33'    # Nodo alma-core

# Lanzadores gr치ficos
alias obsidian="$HOME/apps/obsidian/Obsidian.AppImage &"
alias code-resist='code ~/ALMA_RESIST &'

# Navegaci칩n r치pida
alias cdresist='cd ~/ALMA_RESIST'
alias cdcore='cd ~/ALMA_RESIST/core'
alias cdcontrol='cd ~/ALMA_RESIST/control_central'
alias cdlogs='cd ~/ALMA_RESIST/logs'

# Git
alias gpush='git add . && git commit -m "Backup $(date +\"%Y-%m-%d %H:%M\")" && git push origin master'
alias gpull='git pull'
alias gstatus='git status'
