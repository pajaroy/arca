# ========================================
# Módulo: filesystems.nix
# Montaje de subvolúmenes y particiones base
# ========================================
{ config, pkgs, ... }:

{
  fileSystems."/" = {
    device = "/dev/mapper/alma_core";
    fsType = "btrfs";
    options = [ "subvol=@root" "compress=zstd" ];
  };

  fileSystems."/home" = {
    device = "/dev/mapper/alma_core";
    fsType = "btrfs";
    options = [ "subvol=@home" "compress=zstd" ];
  };

  fileSystems."/boot" = {
    device = "/dev/sdb2";
    fsType = "ext4";
  };

  # (Opcional, para tu "pendrive interno" futuro)
  # fileSystems."/mnt/Pendrive_Interno" = {
  #   device = "/dev/mapper/Pendrive_Interno";
  #   fsType = "ext4";
  # };
}
