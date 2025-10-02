---
tipo: script
id: SCRIPT_2025-06-05_5fa8b6
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Start Server
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:cc6ff5cd9c91d413cec5ee10cebd7a54ab2f9e03b2e6793e2ee37fa9b38ee203
---
#!/bin/bash

# Obtener directorio base del proyecto
BASE_DIR=$(dirname "$(dirname "$(dirname "$(dirname "$(readlink -f "$0")")")")")
VENV_DIR="$BASE_DIR/.venv"
SERVER_DIR="$BASE_DIR/core/llm_server"

# Función para crear contratos
create_contracts() {
    CONTRACTS_DIR="$SERVER_DIR/docs/contracts"
    mkdir -p "$CONTRACTS_DIR"
    
    # Crear schema_prompt.json
    cat > "$CONTRACTS_DIR/schema_prompt.json" <<EOF
{
  "type": "object",
  "properties": {
    "prompt": {"type": "string"},
    "context": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["prompt"]
}
EOF

    # Crear schema_respuesta.json
    cat > "$CONTRACTS_DIR/schema_respuesta.json" <<EOF
{
  "type": "object",
  "properties": {
    "respuesta": {"type": "string"},
    "metadata": {"type": "object"}
  },
  "required": ["respuesta"]
}
EOF
    
    echo "✅ Contratos creados en $CONTRACTS_DIR"
}

# Función para iniciar el servidor
start_server() {
    echo "🔧 Activando entorno virtual..."
    source "$VENV_DIR/bin/activate"
    
    echo "📝 Creando contratos si es necesario..."
    create_contracts
    
    echo "🚀 Iniciando servidor en http://0.0.0.0:8000"
    cd "$BASE_DIR"
    uvicorn core.llm_server.main:app --host 0.0.0.0 --port 8000
}

# Ejecutar
if [ -d "$VENV_DIR" ]; then
    start_server
else
    echo "❌ Error: Entorno virtual no encontrado en $VENV_DIR"
    echo "   Por favor crea un entorno virtual primero:"
    echo "   python -m venv .venv"
    exit 1
fi
