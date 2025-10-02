---
tipo: script
id: SCRIPT_2025-06-05_f3104a
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Ssh Setup
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:e99983b20e9da4cd89db22e80cc0f5e92e1c9ead56e1c538b18c7da120c191e6
---
#!/bin/bash

# ⚙️ Script de configuración de acceso SSH sin contraseña entre nodos ALMA

# 👉 Ejecutar desde alma-core para conectar con alma-resist

DEST_USER="bird"
DEST_IP="192.168.1.36"

echo "🔐 Verificando existencia de clave SSH..."

if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "🔧 Generando nueva clave SSH..."
    ssh-keygen -t ed25519 -C "$USER@alma-core" -f ~/.ssh/id_ed25519 -N ""
else
    echo "✅ Clave existente detectada."
fi

echo "📤 Copiando clave pública a $DEST_USER@$DEST_IP ..."
ssh-copy-id $DEST_USER@$DEST_IP

echo "🔁 Probando conexión SSH..."
ssh $DEST_USER@$DEST_IP "echo '✅ Acceso SSH automático exitoso desde alma-core.'"

echo "✅ Finalizado."
