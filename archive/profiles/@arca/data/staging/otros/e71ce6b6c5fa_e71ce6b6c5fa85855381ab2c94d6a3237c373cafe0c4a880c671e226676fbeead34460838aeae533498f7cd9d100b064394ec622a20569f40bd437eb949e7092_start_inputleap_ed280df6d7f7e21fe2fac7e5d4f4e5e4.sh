---
tipo: script
id: SCRIPT_2025-06-05_62d942
version: '1.0'
formato: sh
modulo: ALMA_RESIST
titulo: Start Inputleap
autor: bird
fecha_creacion: '2025-06-05'
status: activo
version_sistema: Centralesis v2.3
origen: automatico
tags: []
linked_to: []
descripcion: Documento procesado automáticamente
fecha_actualizacion: '2025-06-05'
hash_integridad: sha256:595fa6ea3fa158235edff8ba607bdb56c1cdcc920bcc6234e4c09aee76f37491
---
#!/bin/bash

# 🖱️ Autoejecución de Input Leap con roles invertidos

if [ "$(hostname)" = "alma-resist" ]; then
    input-leaps --no-tray --disable-crypto --name alma-resist --config /home/bird/.input-leap/input-leap.conf &
fi

if [ "$(hostname)" = "alma-core" ]; then
    input-leapc --no-tray --disable-crypto --name alma-core 192.168.1.36:24800 &
fi

