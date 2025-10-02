#!/bin/bash
# Formatea el volumen LUKS con Btrfs y lo monta

set -e

echo "[+] Formateando sistema de archivos en /dev/mapper/alma_crypt..."
mkfs.btrfs -f /dev/mapper/alma_crypt

echo "[+] Montando y creando subvolumen @ para raíz..."
mount /dev/mapper/alma_crypt /mnt
btrfs subvolume create /mnt/@
umount /mnt

echo "[+] Montando subvolumen raíz con compresión zstd..."
mount -o compress=zstd,subvol=@ /dev/mapper/alma_crypt /mnt

echo "[+] Montando partición /boot..."
mkdir -p /mnt/boot
mount /dev/sda1 /mnt/boot

