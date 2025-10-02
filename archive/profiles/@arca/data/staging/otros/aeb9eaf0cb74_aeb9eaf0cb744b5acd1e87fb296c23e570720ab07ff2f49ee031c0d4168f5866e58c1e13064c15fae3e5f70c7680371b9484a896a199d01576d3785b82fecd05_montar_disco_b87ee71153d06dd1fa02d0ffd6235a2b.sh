#!/bin/bash

echo "📦 Montando /dev/mapper/alma_crypt en /mnt"
sudo mount /dev/mapper/alma_crypt /mnt/

echo "💻 Montando /dev/sda2 (EFI) en /mnt/boot/efi..."
sudo mount /dev/sda2 /mnt/boot/efi

echo "✅ Todo montado correctamente."

