#!/bin/bash

# 🖱️ Autoejecución de Input Leap con roles invertidos

if [ "$(hostname)" = "alma-resist" ]; then
    input-leaps --no-tray --disable-crypto --name alma-resist --config /home/bird/.input-leap/input-leap.conf &
fi

if [ "$(hostname)" = "alma-core" ]; then
    input-leapc --no-tray --disable-crypto --name alma-core 192.168.1.36:24800 &
fi

