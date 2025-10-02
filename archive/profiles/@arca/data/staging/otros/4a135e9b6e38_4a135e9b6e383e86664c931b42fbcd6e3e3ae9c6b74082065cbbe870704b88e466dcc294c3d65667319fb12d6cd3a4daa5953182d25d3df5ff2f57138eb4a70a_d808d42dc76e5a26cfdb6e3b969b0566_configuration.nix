# configuration.nix

{ config, pkgs, ... }:

{
  imports = [
    ./hardware-configuration.nix
  ];

  networking.hostName = "alma-resist";
  networking.networkmanager.enable = true;

  i18n.defaultLocale = "en_US.UTF-8";
  time.timeZone = "America/Argentina/Buenos_Aires";

  users.users.alma = {
    isNormalUser = true;
    home = "/home/alma";
    extraGroups = [ "wheel" "networkmanager" ];
    initialPassword = "umamia"; # Cambiala luego
  };

  system.stateVersion = "24.05";
}
