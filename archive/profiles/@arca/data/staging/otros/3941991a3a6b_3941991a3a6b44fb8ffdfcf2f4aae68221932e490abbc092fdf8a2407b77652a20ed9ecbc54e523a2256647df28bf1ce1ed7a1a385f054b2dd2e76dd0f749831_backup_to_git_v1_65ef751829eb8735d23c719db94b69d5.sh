---
tipo: script
id: SCRIPT_2025-06-05_047cd8
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Backup To Git V1
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:56a4e4b472a14238400bc9b8714f0fbafd0918b7f27f85083b6ad91211e01650
---
#!/bin/bash
# 📁 backup_to_git.sh - Respaldo automático con detección de cambios
# Ejecutar: nohup ./backup_to_git.sh > /dev/null 2>&1 &

# ========================
# 🔧 CONFIGURACIÓN GLOBAL
# ========================
BACKUP_DIR="/home/bird/ALMA_RESIST"
REMOTE_REPO="https://github.com/pajaroy/alma_resist"
BRANCH="main"
LOG_FILE="/home/bird/ALMA_RESIST/logs/backup_git/backup_git.log"
PID_FILE="/tmp/backup_to_git.pid"

# ========================
# 🔒 FUNCIONES AUXILIARES
# ========================

init_logging() {
    mkdir -p "$(dirname "$LOG_FILE")"
    touch "$LOG_FILE"
    echo "=== Inicio de sesión: $(date) ===" >> "$LOG_FILE"
}

log() {
    local timestamp
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $1" >> "$LOG_FILE"
}

validate_repo() {
    if [ ! -d "$BACKUP_DIR/.git" ]; then
        log "❌ ERROR: Directorio $BACKUP_DIR no es un repositorio Git"
        echo "Abortando: Ejecuta 'git init' primero" >&2
        exit 1
    fi

    git -C "$BACKUP_DIR" remote show origin >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        log "❌ ERROR: No existe repositorio remoto configurado"
        echo "Abortando: Configura un remoto con 'git remote add'" >&2
        exit 1
    fi
}

check_conflicts() {
    if [ -n "$(git -C "$BACKUP_DIR" diff --name-only --diff-filter=U)" ]; then
        log "⚠️  CONFLICTO: Archivos no fusionados detectados"
        return 1
    fi
    return 0
}

# ========================
# 🚀 FUNCIÓN PRINCIPAL
# ========================
start_backup_daemon() {
    if [ -f "$PID_FILE" ]; then
        if ps -p $(cat "$PID_FILE") > /dev/null; then
            log "⚠️  Script ya en ejecución (PID: $(cat $PID_FILE))"
            exit 0
        fi
    fi
    echo $$ > "$PID_FILE"

    init_logging
    validate_repo
    log "✅ Iniciando monitor de cambios en $BACKUP_DIR"

    inotifywait -m -r -e modify,create,delete,move --exclude '/.git/' "$BACKUP_DIR" |
    while read path action file; do
        log "🔄 Cambio detectado: $action en $file"
        sleep 5

        if ! check_conflicts; then
            log "⏸️  Operación pospuesta por conflictos"
            continue
        fi

        git -C "$BACKUP_DIR" add . >> "$LOG_FILE" 2>&1
        commit_msg="Auto backup $(date +'%Y-%m-%d %H:%M:%S')"
        git -C "$BACKUP_DIR" commit -m "$commit_msg" >> "$LOG_FILE" 2>&1

        if [ $? -eq 0 ]; then
            log "💾 Commit creado: $commit_msg"
            git -C "$BACKUP_DIR" pull --rebase origin "$BRANCH" >> "$LOG_FILE" 2>&1
            git -C "$BACKUP_DIR" push origin "$BRANCH" >> "$LOG_FILE" 2>&1
            if [ $? -eq 0 ]; then
                log "🚀 Push exitoso a $REMOTE_REPO"
            else:
                log "❌ Error en push: Verifica conflictos remotos"
            fi
        else
            log "ℹ️  Sin cambios para commitear"
        fi
    done
}

# ========================
# ⚙️ EJECUCIÓN INICIAL
# ========================
start_backup_daemon
