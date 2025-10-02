#!/bin/bash

echo "🔐 Abriendo disco cifrado /dev/sda3 como alma_crypt..."
sudo cryptsetup luksOpen /dev/sda3 alma_crypt

if [ $? -eq 0 ]; then
    echo "✅ Disco desbloqueado correctamente."
else
    echo "❌ Error al desbloquear el disco."
fi

