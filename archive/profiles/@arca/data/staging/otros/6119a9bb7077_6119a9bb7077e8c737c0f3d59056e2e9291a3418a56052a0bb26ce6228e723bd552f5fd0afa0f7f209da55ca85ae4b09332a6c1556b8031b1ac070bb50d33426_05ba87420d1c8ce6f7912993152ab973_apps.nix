# ========================================
# Módulo: apps.nix
# Descripción: Instalación de paquetes, utilidades y servicios principales.
# Responsable: Bird
# Creado: 2024-06-30
# Versión: 0.1.0
# ========================================

{ config, pkgs, ... }:

{
      environment.systemPackages = with pkgs; [
    vim
    wget
    git
    python3
    tree
    htop
    curl
    btrfs-progs
    parted
    zip
    unzip
    p7zip
    gnupg
    age
    nano
    nix-index
    openssh
    syncthing
    vscode-fhs
  ];

}