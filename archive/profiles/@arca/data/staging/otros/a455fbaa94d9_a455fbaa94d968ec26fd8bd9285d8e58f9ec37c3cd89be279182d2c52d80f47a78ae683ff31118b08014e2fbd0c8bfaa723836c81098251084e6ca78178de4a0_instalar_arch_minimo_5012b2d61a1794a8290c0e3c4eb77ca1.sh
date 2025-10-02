#!/bin/bash

echo "==> Montando partición raíz en /mnt"
mount /dev/sda1 /mnt

echo "==> Activando partición swap"
swapon /dev/sda2

echo "==> Instalando sistema base..."
pacstrap /mnt base linux linux-firmware vim nano sudo grub

echo "==> Generando fstab..."
genfstab -U /mnt >> /mnt/etc/fstab

echo "==> Instalación mínima completada. Podés chrootear con:"
echo "    arch-chroot /mnt"

