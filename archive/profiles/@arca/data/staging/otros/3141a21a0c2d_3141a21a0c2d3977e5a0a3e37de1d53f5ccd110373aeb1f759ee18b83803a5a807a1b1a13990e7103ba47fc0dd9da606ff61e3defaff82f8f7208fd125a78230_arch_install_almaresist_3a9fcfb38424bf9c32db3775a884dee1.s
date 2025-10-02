#!/bin/bash
# Script de instalación de Arch Linux con LUKS, Btrfs y GRUB UEFI
# Asumimos que las particiones ya están hechas: sda1 (EFI), sda2 (swap), sda3 (LUKS)

set -e

echo "[1/9] Desbloqueando disco cifrado..."
cryptsetup luksOpen /dev/sda3 cryptroot

echo "[2/9] Montando Btrfs..."
mount -o subvol=@ /dev/mapper/cryptroot /mnt
mkdir -p /mnt/{boot,home}
mount -o subvol=@home /dev/mapper/cryptroot /mnt/home

echo "[3/9] Montando partición EFI..."
mount /dev/sda1 /mnt/boot

echo "[4/9] Instalando paquetes base..."
pacstrap -K /mnt base linux linux-firmware btrfs-progs sudo vim networkmanager grub efibootmgr

echo "[5/9] Generando fstab..."
genfstab -U /mnt >> /mnt/etc/fstab

echo "[6/9] Entrando al sistema..."
arch-chroot /mnt /bin/bash <<'EOF'
  echo "[6.1] Estableciendo zona horaria..."
  ln -sf /usr/share/zoneinfo/America/Argentina/Buenos_Aires /etc/localtime
  hwclock --systohc

  echo "[6.2] Configurando locales..."
  sed -i 's/^#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
  locale-gen
  echo "LANG=en_US.UTF-8" > /etc/locale.conf

  echo "[6.3] Configurando hostname..."
  echo "almaresist" > /etc/hostname

  echo "[6.4] Configurando red..."
  systemctl enable NetworkManager

  echo "[6.5] Instalando GRUB en modo UEFI..."
  grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
  echo 'GRUB_CMDLINE_LINUX="cryptdevice=UUID=$(blkid -s UUID -o value /dev/sda3):cryptroot root=/dev/mapper/cryptroot"' >> /etc/default/grub
  grub-mkconfig -o /boot/grub/grub.cfg

  echo "[6.6] Creando usuario y seteando root..."
  echo root:almaresist | chpasswd
  useradd -m -G wheel santi
  echo santi:almaresist | chpasswd
  sed -i 's/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers
EOF

echo "[7/9] Hecho. Desmontando..."
umount -R /mnt
cryptsetup close cryptroot

echo "[8/9] Instalación completada. Reiniciando..."
reboot
