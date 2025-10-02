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


  networking.hostName = "sv_alma";
  networking.networkmanager.enable = true;

  i18n.defaultLocale = "en_US.UTF-8";
  console.keyMap = "la-latin1";

  time.timeZone = "America/Argentina/Buenos_Aires";

  uders.groups."alma" = {};

  users.users."sv_alma" = {
    isNormalUser = true;
    home = "/home/sv_alma";
    group = "alma";
    extraGroups = [ "wheel" "networkmanager" ];
    initialPassword = "umamia";
    shell = pkgs.bash;
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

