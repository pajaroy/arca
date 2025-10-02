#!/bin/bash
# @arca-cleaner.sh
# Descripción: Elimina archivos duplicados exactos en processed/ conservando 1 copia
# Uso: ./cleaner.sh

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================
BASE_DIR="${1:-$HOME/@arca}"
PROCESSED_DIR="${BASE_DIR}/.source/og/processed"
BACKUP_DIR="${BASE_DIR}/.source/og/duplicates_backup"
LOG_FILE="${BASE_DIR}/.source/logs/source.log"

# Verificar dependencias
if ! command -v fdupes &> /dev/null; then
    echo "❌ Error: fdupes no está instalado. Instala con:"
    echo "  sudo apt install fdupes"
    exit 1
fi

# ==============================================================================
# FUNCIÓN PRINCIPAL
# ==============================================================================
clean_duplicates() {
    echo "[$(date)] Iniciando limpieza de duplicados en ${PROCESSED_DIR}" | tee -a "$LOG_FILE"
    
    # Crear directorio de backup
    mkdir -p "$BACKUP_DIR"
    
    # Ejecutar fdupes y procesar resultados
    fdupes -rf "$PROCESSED_DIR" | while read -r file; do
        if [[ -f "$file" ]]; then
            # Generar ruta de backup manteniendo estructura
            rel_path="${file#$PROCESSED_DIR/}"
            backup_path="${BACKUP_DIR}/${rel_path}"
            mkdir -p "$(dirname "$backup_path")"
            
            # Mover a backup y registrar
            if mv "$file" "$backup_path"; then
                echo "$(date +%FT%T),DUPLICADO,${file},${backup_path}" >> "$LOG_FILE"
                echo "♻️  Duplicado movido: ${file} → ${backup_path}"
            else
                echo "❌ Error moviendo duplicado: ${file}" | tee -a "$LOG_FILE"
            fi
        fi
    done
    
    echo "[$(date)] Limpieza completada. Duplicados guardados en ${BACKUP_DIR}" | tee -a "$LOG_FILE"
}

# ==============================================================================
# EJECUCIÓN
# ==============================================================================
main() {
    echo "=== INICIO LIMPIEZA DUPLICADOS: $(date) ===" >> "$LOG_FILE"
    
    if [[ ! -d "$PROCESSED_DIR" ]]; then
        echo "❌ Error: Directorio processed no encontrado" | tee -a "$LOG_FILE"
        exit 1
    fi
    
    clean_duplicates
    
    echo "=== RESUMEN ==="
    echo "Duplicados movidos a: ${BACKUP_DIR}"
    echo "Registro completo en: ${LOG_FILE}"
    echo "=== FIN LIMPIEZA: $(date) ===" >> "$LOG_FILE"
}

main "$@"