---
tipo: script
id: SCRIPT_2025-06-05_c9ff5c
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Chat
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:bf74662995f2c4dd813a8c96fb099b60f1d77733c5af21d00ae833d3435547aa
---
#!/bin/bash

# Configuración avanzada
API_URL="http://localhost:8000/responder"
SESSION_ID="alma-$(date +%s)"
HISTORY_FILE="/tmp/alma_chat_$SESSION_ID.txt"
DEBUG_LOG="/tmp/alma_chat_debug.log"
MAX_HISTORY_LINES=100
USER_NAME="Tú"
BOT_NAME="ALMA"

# Paleta de colores moderna
DARK_BG='\033[48;2;30;30;46m'
LIGHT_BG='\033[48;2;49;50;68m'
USER_COLOR='\033[38;2;166;227;161m'
BOT_COLOR='\033[38;2;137;180;250m'
TIMESTAMP_COLOR='\033[38;2;180;190;254m'
INPUT_COLOR='\033[38;2;243;139;168m'
ERROR_COLOR='\033[38;2;243;139;168m'
SYSTEM_COLOR='\033[38;2;245;194;231m'
RESET='\033[0m'

# Configuración de UI
TERMINAL_WIDTH=$(tput cols)
BUBBLE_WIDTH=$((TERMINAL_WIDTH - 10))
LINE_LENGTH=$((BUBBLE_WIDTH - 8))

# Inicialización
touch "$HISTORY_FILE"
touch "$DEBUG_LOG"
echo -e "\n${SYSTEM_COLOR}Iniciando sesión de chat - $(date)${RESET}" >> "$DEBUG_LOG"

# Función para mostrar mensajes con efecto de máquina de escribir
typewriter() {
    local text="$1"
    local color="$2"
    local delay=0.02
    
    echo -en "${color}"
    for ((i=0; i<${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep $delay
    done
    echo -e "${RESET}"
}

# Función para formatear burbujas de chat
format_chat_bubble() {
    local sender="$1"
    local message="$2"
    local timestamp="$3"
    local color
    local name
    
    if [[ "$sender" == "user" ]]; then
        color="$USER_COLOR"
        name="$USER_NAME"
        align="right"
    else
        color="$BOT_COLOR"
        name="$BOT_NAME"
        align="left"
    fi
    
    # Formato de tiempo relativo
    local now=$(date +%s)
    local diff=$((now - timestamp))
    local time_ago
    
    if ((diff < 60)); then
        time_ago="hace unos segundos"
    elif ((diff < 3600)); then
        local mins=$((diff / 60))
        time_ago="hace $mins min"
    else
        time_ago="hace $((diff / 3600)) horas"
    fi
    
    # Crear burbuja
    echo -e "${TIMESTAMP_COLOR}${time_ago}${RESET}"
    echo -e "${DARK_BG}${color}${RESET}${color}${DARK_BG} ${name} ${RESET}"
    
    # Dividir mensaje en líneas
    fold -w $LINE_LENGTH -s <<< "$message" | while IFS= read -r line; do
        # Espaciado para alineación
        if [[ "$align" == "right" ]]; then
            local padding=$((BUBBLE_WIDTH - ${#line} - 4))
            printf "${color}${DARK_BG}%${padding}s${line}   ${RESET}\n" ""
        else
            echo -e "${color}${DARK_BG}   ${line}${RESET}"
        fi
    done
    
    echo -e "${color}${DARK_BG}${RESET}"
    echo
}

# Función para mostrar el historial de chat
display_chat_history() {
    clear
    echo -e "${DARK_BG}${SYSTEM_COLOR}"
    echo "╭──────────────────────────────────────────────────────────╮"
    echo "│               $BOT_NAME - Asistente Virtual               │"
    echo "╰──────────────────────────────────────────────────────────╯"
    echo -e "${RESET}"
    
    if [[ ! -f "$HISTORY_FILE" ]] || [[ ! -s "$HISTORY_FILE" ]]; then
        echo -e "\n${SYSTEM_COLOR}No hay mensajes en el historial${RESET}"
        return
    fi
    
    # Leer historial en reversa (los más nuevos primero)
    tac "$HISTORY_FILE" | while IFS= read -r line; do
        if [[ -z "$line" ]]; then continue; fi
        
        local type="${line:0:4}"
        local content="${line:5}"
        
        if [[ "$type" == "MSG|" ]]; then
            IFS='|' read -r sender message timestamp <<< "$content"
            format_chat_bubble "$sender" "$message" "$timestamp"
        elif [[ "$type" == "SYS|" ]]; then
            echo -e "${SYSTEM_COLOR}${content}${RESET}"
        fi
    done
}

# Función para enviar mensajes a la API
send_to_alma() {
    local prompt="$1"
    
    # Escapar contenido usando jq
    local json_payload
    json_payload=$(jq -n --arg prompt "$prompt" '{"prompt": $prompt}')
    
    if [ $? -ne 0 ]; then
        echo "SYS|Error al formatear el prompt a JSON" >> "$HISTORY_FILE"
        return 1
    fi
    
    # Enviar usando curl
    local response
    response=$(curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d "$json_payload" 2>>"$DEBUG_LOG")
    local curl_exit=$?
    
    if [ $curl_exit -ne 0 ]; then
        echo "SYS|Error de red al conectar con el servidor (código: $curl_exit)" >> "$HISTORY_FILE"
        return 1
    fi
    
    # Extraer respuesta
    local answer
    answer=$(echo "$response" | jq -r '.respuesta')
    local jq_exit=$?
    
    if [ $jq_exit -ne 0 ]; then
        echo "SYS|Error al parsear la respuesta del servidor" >> "$HISTORY_FILE"
        echo "SYS|Respuesta cruda: $response" >> "$HISTORY_FILE"
        return 1
    fi
    
    if [ "$answer" == "null" ] || [ -z "$answer" ]; then
        echo "SYS|Error: Respuesta vacía o nula del servidor" >> "$HISTORY_FILE"
        return 1
    fi
    
    echo "$answer"
}

# Función para entrada de texto multi-línea
multi_line_input() {
    local prompt="$1"
    local input=""
    
    echo -e "${INPUT_COLOR}${prompt} (Ctrl+D para enviar)${RESET}"
    echo -e "${USER_COLOR}${DARK_BG}${RESET}${USER_COLOR}${DARK_BG} $USER_NAME ${RESET}"
    
    while IFS= read -r line; do
        input="$input$line\n"
        echo -e "${USER_COLOR}${DARK_BG}   ${line}${RESET}"
    done
    
    echo -e "${USER_COLOR}${DARK_BG}${RESET}"
    
    # Remover el último newline
    echo -n "${input%\\n}"
}

# Función principal de chat
chat_loop() {
    # Mensaje de bienvenida
    local welcome_msg="¡Hola! Soy $BOT_NAME, tu asistente virtual. ¿En qué puedo ayudarte hoy?"
    local ts=$(date +%s)
    echo "MSG|bot|$welcome_msg|$ts" >> "$HISTORY_FILE"
    
    while true; do
        display_chat_history
        
        # Entrada de usuario con soporte multi-línea
        echo -e "\n${INPUT_COLOR}Escribe tu mensaje:${RESET}"
        user_input=$(multi_line_input)
        
        # Manejar comandos especiales
        case "$(echo "$user_input" | tr '[:upper:]' '[:lower:]')" in
            "/salir"|"/exit")
                echo "SYS|Sesión finalizada" >> "$HISTORY_FILE"
                return 0
                ;;
            "/limpiar"|"/clear")
                > "$HISTORY_FILE"
                continue
                ;;
            "/debug")
                echo "SYS|Mostrando logs de depuración" >> "$HISTORY_FILE"
                echo "SYS|=== ÚLTIMOS ERRORES ===" >> "$HISTORY_FILE"
                tail -n 5 "$DEBUG_LOG" >> "$HISTORY_FILE"
                echo "SYS|======================" >> "$HISTORY_FILE"
                continue
                ;;
            "/ayuda"|"/help")
                echo "SYS|Comandos disponibles:" >> "$HISTORY_FILE"
                echo "SYS|/salir - Terminar sesión" >> "$HISTORY_FILE"
                echo "SYS|/limpiar - Borrar historial" >> "$HISTORY_FILE"
                echo "SYS|/debug - Mostrar errores" >> "$HISTORY_FILE"
                echo "SYS|/ayuda - Mostrar esta ayuda" >> "$HISTORY_FILE"
                continue
                ;;
        esac
        
        # Guardar mensaje de usuario
        local ts=$(date +%s)
        echo "MSG|user|$user_input|$ts" >> "$HISTORY_FILE"
        
        # Mantener tamaño del historial
        tail -n $MAX_HISTORY_LINES "$HISTORY_FILE" > "$HISTORY_FILE.tmp"
        mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"
        
        # Enviar a ALMA con animación
        display_chat_history
        echo -e "\n${SYSTEM_COLOR}$BOT_NAME está escribiendo...${RESET}"
        
        # Obtener respuesta
        response=$(send_to_alma "$user_input")
        
        if [ $? -eq 0 ]; then
            # Guardar respuesta
            local ts=$(date +%s)
            echo "MSG|bot|$response|$ts" >> "$HISTORY_FILE"
            
            # Mantener tamaño del historial
            tail -n $MAX_HISTORY_LINES "$HISTORY_FILE" > "$HISTORY_FILE.tmp"
            mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"
        else
            echo "SYS|Error al obtener respuesta del servidor" >> "$HISTORY_FILE"
        fi
    done
}

# Limpiar al salir
cleanup() {
    echo -e "\n${SYSTEM_COLOR}Guardando historial completo en: ~/alma_chat_$SESSION_ID.txt${RESET}"
    cp "$HISTORY_FILE" "$HOME/alma_chat_$SESSION_ID.txt"
    rm -f "$HISTORY_FILE"
    echo -e "${SYSTEM_COLOR}Sesión finalizada. ¡Hasta pronto!${RESET}"
}
trap cleanup EXIT

# Verificar dependencias
check_dependencies() {
    local missing=0
    
    if ! command -v jq &> /dev/null; then
        echo -e "${ERROR_COLOR}❌ Error: Necesitas instalar 'jq' para procesar JSON${RESET}"
        echo "   Instala con: sudo apt install jq"
        missing=1
    fi
    
    if ! command -v curl &> /dev/null; then
        echo -e "${ERROR_COLOR}❌ Error: Necesitas instalar 'curl' para hacer peticiones HTTP${RESET}"
        echo "   Instala con: sudo apt install curl"
        missing=1
    fi
    
    if ! command -v fold &> /dev/null; then
        echo -e "${ERROR_COLOR}❌ Error: Necesitas instalar 'fold' para formatear texto${RESET}"
        echo "   Generalmente viene instalado en sistemas Unix"
        missing=1
    fi
    
    return $missing
}

# Animación de inicio
startup_animation() {
    clear
    echo -e "${DARK_BG}"
    echo "╭──────────────────────────────────────────────────────────╮"
    echo "│                                                        │"
    echo "│   ${BOT_COLOR} █████╗ ██╗     ███╗   ███╗ █████╗ ${SYSTEM_COLOR}██████╗ ███████╗${RESET}${DARK_BG}   │"
    echo "│   ${BOT_COLOR}██╔══██╗██║     ████╗ ████║██╔══██╗${SYSTEM_COLOR}██╔══██╗██╔════╝${RESET}${DARK_BG}   │"
    echo "│   ${BOT_COLOR}███████║██║     ██╔████╔██║███████║${SYSTEM_COLOR}██████╔╝███████╗${RESET}${DARK_BG}   │"
    echo "│   ${BOT_COLOR}██╔══██║██║     ██║╚██╔╝██║██╔══██║${SYSTEM_COLOR}██╔══██╗╚════██║${RESET}${DARK_BG}   │"
    echo "│   ${BOT_COLOR}██║  ██║███████╗██║ ╚═╝ ██║██║  ██║${SYSTEM_COLOR}██║  ██║███████║${RESET}${DARK_BG}   │"
    echo "│   ${BOT_COLOR}╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝${SYSTEM_COLOR}╚═╝  ╚═╝╚══════╝${RESET}${DARK_BG}   │"
    echo "│                                                        │"
    echo "│                ${SYSTEM_COLOR}Asistente Virtual Terminal${RESET}${DARK_BG}               │"
    echo "│                                                        │"
    echo "╰──────────────────────────────────────────────────────────╯"
    echo -e "${RESET}"
    
    for i in {1..5}; do
        echo -ne "${SYSTEM_COLOR}Iniciando sistema${RESET}${TIMESTAMP_COLOR} [${RESET}"
        for j in $(seq 1 $i); do
            echo -ne "${SYSTEM_COLOR}■${RESET}"
        done
        for j in $(seq $i 4); do
            echo -ne " "
        done
        echo -ne "${TIMESTAMP_COLOR}]${RESET}"
        sleep 0.2
        echo -ne "\r"
    done
    echo
}

# Inicio del script
if check_dependencies; then
    startup_animation
    sleep 1.5
    chat_loop
else
    exit 1
fi
