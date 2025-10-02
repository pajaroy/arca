# ========================================
# Módulo: filesystems.nix
# Montaje de subvolúmenes y particiones base
# ========================================
{ config, pkgs, ... }:

{
  fileSystems."/" = {
    device = "/dev/mapper/alma_crypt";
    fsType = "btrfs";
    options = [ "compress=zstd" ];
  };

  fileSystems."/home" = {
    device = "/dev/mapper/alma_crypt";
    fsType = "btrfs";
    options = [ "subvol=@home" "compress=zstd" ];
  };

  fileSystems."/boot" = {
    device = "/dev/sdb2";
    fsType = "ext4";
  };

}
