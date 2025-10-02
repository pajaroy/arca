#!/bin/bash

# === CONFIGURACIÓN GENERAL ===
REMOTE_NAME="remote" # Cambiar por el nombre de tu remote rclone si es distinto
LOG_DIR="$HOME/ALMA_LOGS"
FECHA=$(date +'%Y-%m-%d_%H-%M')
mkdir -p "$LOG_DIR"

# === RUTAS LOCALES ===
ALMA_DIR="$HOME/Documentos/ALMA_LIBRE"
CUADERNO_13CC="$ALMA_DIR/CUADERNOS/13CC.cu"
EMPRESA_13CC="$ALMA_DIR/EMPRESAS/13CC.em"

# === RUTAS EN DRIVE ===
DRIVE_BASE="$REMOTE_NAME:ALMA_BACKUP"
DRIVE_13CC_CU="$DRIVE_BASE/13CC.cu"
DRIVE_13CC_EM="$DRIVE_BASE/13CC.em"
DRIVE_ALMA="$DRIVE_BASE/ALMA_LIBRE"

# === FUNCIÓN DE SINCRONIZACIÓN ===
sync_folder() {
    SRC="$1"
    DEST="$2"
    LABEL="$3"
    echo "🔄 Sincronizando $LABEL..."
    rclone sync "$SRC" "$DEST" --progress --create-empty-src-dirs --log-file="$LOG_DIR/sync_$LABEL_$FECHA.log" --log-level INFO
    echo "✅ $LABEL sincronizado. Log: $LOG_DIR/sync_$LABEL_$FECHA.log"
}

# === MENÚ DE OPCIONES ===
menu_manual() {
    echo "Seleccione una opción de sincronización:"
    echo "1) Solo 13CC.cu"
    echo "2) Solo 13CC.em"
    echo "3) Toda la carpeta ALMA_LIBRE"
    echo "4) TODO (cuaderno + empresa + sistema)"
    read -p "Opción: " opcion

    case $opcion in
        1) sync_folder "$CUADERNO_13CC" "$DRIVE_13CC_CU" "13CC_cu";;
        2) sync_folder "$EMPRESA_13CC" "$DRIVE_13CC_EM" "13CC_em";;
        3) sync_folder "$ALMA_DIR" "$DRIVE_ALMA" "ALMA_LIBRE";;
        4)
            sync_folder "$CUADERNO_13CC" "$DRIVE_13CC_CU" "13CC_cu"
            sync_folder "$EMPRESA_13CC" "$DRIVE_13CC_EM" "13CC_em"
            sync_folder "$ALMA_DIR" "$DRIVE_ALMA" "ALMA_LIBRE"
            ;;
        *) echo "❌ Opción inválida"; exit 1;;
    esac
}

# === MODO AUTOMÁTICO O MANUAL ===
if [[ "$1" == "--auto" ]]; then
    echo "🔁 Modo automático: sincronizando todo..."
    sync_folder "$CUADERNO_13CC" "$DRIVE_13CC_CU" "13CC_cu"
    sync_folder "$EMPRESA_13CC" "$DRIVE_13CC_EM" "13CC_em"
    sync_folder "$ALMA_DIR" "$DRIVE_ALMA" "ALMA_LIBRE"
elif [[ "$1" == "--menu" ]]; then
    menu_manual
else
    echo "Uso:"
    echo "  ./sync_alma_drive.sh --menu     # Modo interactivo"
    echo "  ./sync_alma_drive.sh --auto     # Modo automático (todo)"
    exit 1
fi
