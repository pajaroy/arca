#!/bin/bash
# @arca-file-classifier.sh - Versión portable
# Uso: ./classifier.sh [RUTA_BASE]

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

# 1. Ruta base (argumento o default)
BASE_DIR="${1:-$HOME/@arca}"
if [[ ! -d "$BASE_DIR" ]]; then
    echo "❌ Error: Directorio base no encontrado: $BASE_DIR" >&2
    echo "   Uso: $0 [ruta_base_arca]" >&2
    exit 1
fi

# 2. Rutas derivadas
SOURCE_DIR="${BASE_DIR}/.source/og/archivo"
DEST_DIR="${BASE_DIR}/.source/og/processed"
LOG_FILE="${BASE_DIR}/.source/logs/source.log"
mkdir -p "$SOURCE_DIR" "$DEST_DIR" "${BASE_DIR}/.source/logs"

# 3. Extensiones (personalizable)
declare -A EXT_MAP=(
    [".py"]="python"
    [".yaml"]="yaml"
    [".yml"]="yaml"
    [".md"]="markdown"
    [".sql"]="sql"
    [".csv"]="csv"
)

# ==============================================================================
# FUNCIÓN PRINCIPAL
# ==============================================================================
classify_files() {
    echo "[$(date)] Iniciando clasificación en ${BASE_DIR}..." | tee -a "$LOG_FILE"
    
    # Crear estructura de directorios
    for dir in "${EXT_MAP[@]}" otros; do
        mkdir -p "${DEST_DIR}/${dir}"
    done
    
    # Procesar archivos
    find "$SOURCE_DIR" -type f | while read -r file; do
        filename=$(basename "$file")
        ext=".${filename##*.}"
        category="${EXT_MAP[$ext]:-otros}"
        dest_path="${DEST_DIR}/${category}/${filename}"
        
        # Verificar duplicados
        if [[ -f "$dest_path" ]]; then
            echo "⚠️  Duplicado: ${filename} (saltando)" | tee -a "$LOG_FILE"
            continue
        fi
        
        # Mover y registrar
        if mv -n "$file" "$dest_path" 2>/dev/null; then
            hash=$(blake3 "$dest_path" | cut -d' ' -f1)
            echo "$(date +%FT%T),${dest_path},${hash},${category}" >> "$LOG_FILE"
            echo "✅ ${filename} → ${category}"
        else
            echo "❌ Error moviendo ${filename}" | tee -a "$LOG_FILE"
        fi
    done
}

# ==============================================================================
# EJECUCIÓN
# ==============================================================================
main() {
    echo "=== INICIO: $(date) ===" >> "$LOG_FILE"
    echo "BASE_DIR: $BASE_DIR" >> "$LOG_FILE"
    
    classify_files
    
    echo "=== RESUMEN ==="
    echo "Clasificación completada en: $DEST_DIR"
    echo "Log unificado: $LOG_FILE"
    echo "=== FIN: $(date) ===" >> "$LOG_FILE"
}

main "$@"