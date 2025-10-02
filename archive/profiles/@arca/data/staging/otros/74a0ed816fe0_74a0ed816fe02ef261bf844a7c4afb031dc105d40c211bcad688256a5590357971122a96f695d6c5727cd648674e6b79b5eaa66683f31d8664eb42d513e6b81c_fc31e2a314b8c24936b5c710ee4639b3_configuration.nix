{ config, pkgs, ... }:

{
  imports =
    [ ./hardware-configuration.nix ];
  #==========================================================#
  #           Configuracion Base Encriptada v0.0.1           #
  #==========================================================#

  # Bootloader EFI
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;


  networking.hostName = "cc13";
  networking.networkmanager.enable = true;

  i18n.defaultLocale = "en_US.UTF-8";
  console.keyMap = "la-latin1";

  time.timeZone = "America/Argentina/Buenos_Aires";

  users.users.alma = {
    isNormalUser = true;
    home = "/home/cc13";
    extraGroups = [ "wheel" "networkmanager" ];
    initialPassword = "umamia";
  };
  #=========================================================#
  #                   Sincronizacion                        #
  #=========================================================#

  services.openssh.enable = false; # por ahora off

  #=========================================================#
  #                    Aplicaciones                         #
  #=========================================================#
 
  environment.systemPackages = with pkgs; [
    vim
    wget
    git
  ];

  #=========================================================#
  # Version :
  system.stateVersion = "23.11";
  #=========================================================#
}

