# hardware_configuration

{ config, lib, pkgs, ... }:

{
  imports = [ ];

  # Kernel y hardware detectados por nixos-generate-config
  boot.initrd.availableKernelModules = [ "xhci_pci" "ahci" "ohci_pci" "ehci_pci" "usbhid" "usb_storage" "sd_mod" ];
  boot.initrd.kernelModules = [ ];
  boot.kernelModules = [ "kvm-amd" ];
  boot.extraModulePackages = [ ];

  # LUKS: nombre y device (clave para btrfs root cifrado)
  boot.initrd.luks.devices."alma_core".device = "/dev/sda3";

  # Mapeo de filesystems (subvolúmenes Btrfs + boot)
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
    device = "/dev/sda2";
    fsType = "vfat"; # O "ext4" si la formateaste así (verificalo con `lsblk -f`)
  };

  swapDevices = [ ];

  nixpkgs.hostPlatform = lib.mkDefault "x86_64-linux";
  hardware.cpu.amd.updateMicrocode = lib.mkDefault config.hardware.enableRedistributableFirmware;
}
