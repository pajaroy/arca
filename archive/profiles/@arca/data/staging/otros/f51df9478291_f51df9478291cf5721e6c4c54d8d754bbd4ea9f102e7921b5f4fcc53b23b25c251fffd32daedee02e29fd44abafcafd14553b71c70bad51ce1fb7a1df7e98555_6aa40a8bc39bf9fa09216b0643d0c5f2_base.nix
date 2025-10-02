# ========================================
# Módulo: base.nix
# Configuración base de ALMA_RESIST
# ========================================
{ config, pkgs, ... }:

{
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  # LUKS para raíz
  boot.initrd.luks.devices."alma_crypt".device = "/dev/sdb3"; # Cambiar según host/disco
  # Si preferís UUID, reemplazá por: "UUID-xxxx..."

  networking.hostName = "alma-resist";
  networking.networkmanager.enable = true;
  networking.firewall.allowedTCPPorts = [ 22000 ];
  networking.firewall.allowedUDPPorts = [ 22000 ];

  i18n.defaultLocale = "en_US.UTF-8";
  console.keyMap = "la-latin1";

  time.timeZone = "America/Argentina/Buenos_Aires";

  users.users.alma = {
    isNormalUser = true;
    home = "/home/alma";
    group = "alma";
    extraGroups = [ "wheel" "networkmanager" ];
    initialPassword = "umamia";  # Cambiala después
  };

  users.groups.alma = {};

  system.stateVersion = "23.11";
}
