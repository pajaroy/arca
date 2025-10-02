#!/bin/bash
# @arca-file-indexer.sh
# Descripción: Clasificador automático de archivos para el sistema @arca
# Dependencias: python3, jq, b3sum, fdupes
# Funcionalidades:
# 1. Clasifica archivos por extensión en carpetas específicas
# 2. Genera metadatos clave (hash, fecha, tamaño)
# 3. Elimina duplicados manteniendo un registro completo
# Uso: ./arca-file-indexer.sh (ejecutar desde cualquier ubicación)

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================
function load_config() {
    local yaml_file="$HOME/@arca/.source/config/config.yaml"
    if [[ ! -f "$yaml_file" ]]; then
        echo "[ERROR] Archivo de configuración no encontrado: $yaml_file" >> "$LOG_FILE"
        exit 1
    fi
    
    # Usamos python para validar y cargar
    config_json=$(python3 -c "
import yaml, json, sys; 
try:
    cfg = yaml.safe_load(open('$yaml_file'))
    print(json.dumps(cfg))
except Exception as e:
    print(f'ERROR: {str(e)}', file=sys.stderr)
    exit(1)
")
    
    if [[ "$config_json" == ERROR* ]]; then
        echo "[ERROR] Configuración YAML inválida: ${config_json:6}" >> "$LOG_FILE"
        exit 1
    fi
    
    # Convertir JSON a variables bash
    declare -gA config
    while IFS="=" read -r key value; do
        config["$key"]="$value"
    done < <(jq -r 'paths(scalars) as $p | "\($p|join("_"))=\(getpath($p))"' <<< "$config_json")
}

# ==============================================================================
# INICIALIZACIÓN
# ==============================================================================
init_dirs() {
    mkdir -p "${config[paths_directorios_formato]}"
    for categoria in "${!config[@]}"; do
        if [[ "$categoria" =~ ^formatos_categorias_ ]]; then
            mkdir -p "${config[paths_directorios_formato]}/${categoria#formatos_categorias_}"
        fi
    done
}

# ==============================================================================
# FUNCIONES PRINCIPALES
# ==============================================================================

function setup_csv() {
    # Generar headers desde config.yaml
    headers=$(IFS=,; echo "${config[metadata_campos_obligatorios[*]}")
    echo "$headers" > "$METADATA_CSV"
}

function classify_file() {
    local file="$1"
    local ext="${file##*.}"
    
    # Buscar en categorías definidas
    for categoria in "${!config[@]}"; do
        if [[ "$categoria" =~ ^formatos_categorias_ ]]; then
            local cat_name="${categoria#formatos_categorias_}"
            if [[ " ${config[$categoria]} " =~ " .$ext " ]]; then
                echo "$FORMATO_DIR/$cat_name"
                return
            fi
        fi
    done
    
    echo "$FORMATO_DIR/otros"
}

process_metadata() {
    local file="$1"
    local dest="$2"
    
    # Validar extensiones ignoradas
    if [[ " ${config[metadata_formatos_especiales_ignorar]} " =~ " .${file##*.} " ]]; then
        return
    fi

    # Generar metadatos
    local -A meta=(
        ["ruta"]="${dest#$HOME/@arca}"
        ["nombre"]="$(basename "$file")"
        ["tipo"]="${dest##*/}"
        ["tamano_bytes"]="$(stat -c%s "$file")"
        ["fecha_mod"]="$(date -r "$file" +"%Y-%m-%dT%H:%M:%S")"
        ["hash_blake3"]="$(b3sum "$file" | cut -d' ' -f1)"
    )

    # Escribir CSV
    local csv_line
    IFS=, read -r -a campos <<< "${config[metadata_campos_obligatorios]}"
    for campo in "${campos[@]}"; do
        csv_line+="${meta[$campo]},"
    done
    echo "${csv_line%,}" >> "$METADATA_CSV"
}

