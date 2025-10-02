# ========================================
# Módulo: xfce.nix
# Configura XFCE, LightDM y layout X11
# ========================================
{ config, pkgs, ... }:

{
  services.xserver.enable = true;
  services.xserver.displayManager.lightdm.enable = true;
  services.xserver.desktopManager.xfce.enable = true;
  services.xserver.xkb.layout = "latam"; # Cambiá por "us" si preferís
}
