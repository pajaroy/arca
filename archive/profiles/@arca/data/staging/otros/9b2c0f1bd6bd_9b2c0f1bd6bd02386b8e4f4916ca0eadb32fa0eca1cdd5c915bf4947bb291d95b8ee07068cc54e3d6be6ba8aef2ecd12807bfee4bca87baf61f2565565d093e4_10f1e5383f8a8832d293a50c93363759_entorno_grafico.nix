{ config, pkgs, ... }:

{
  # Habilitar entorno gráfico básico con XFCE y LightDM
  services.xserver.enable = true;
  services.xserver.displayManager.lightdm.enable = true;
  services.xserver.desktopManager.xfce.enable = true;
  services.xserver.layout = "latam";

  # Soporte touchpad (opcional, borra si solo usás PC de escritorio)
  services.xserver.libinput.enable = true;

  # Paquetes gráficos esenciales
  environment.systemPackages = with pkgs; [
    xfce4-terminal     # Terminal gráfica de XFCE
    mousepad           # Editor de texto liviano
    thunar             # Gestor de archivos gráfico
  ];
}
