# -----------------------------------------
# NixOS Configuration - ALMA_RESIST v0.0.3
# -----------------------------------------

# -----------------------------------------
# Imports
# -----------------------------------------

# Import hardware configuration
{ config, pkgs, ... }:

{
  imports =
    [
      ./hardware-configuration.nix
    ];

# -----------------------------------------
# Boot Loader
# -----------------------------------------

  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  boot.loader.efi.efiSysMountPoint = "/boot";

# -----------------------------------------
# File Systems
# -----------------------------------------

 fileSystems."/" = {
   device = "/dev/mapper/alma_crypt";
   fsType = "btrfs";
   options = [ "compress=zstd" ];
 };

 fileSystems."/boot" = {
   device = "/dev/sda2";
   fsType = "vfat";
   options = [ "fmask=0022" "dmask=0022" ];
 };

# -----------------------------------------
# Networking
# -----------------------------------------

  networking.hostName = "alma-resist";
  networking.networkmanager.enable = true;

  # Firewall enabled
  networking.firewall = {
    enable = true;
    allowedTCPPorts = [ 22 ]; # SSH
    # Tailscale might require UDP 41641, leave commented for now
    # allowedUDPPorts = [ 41641 ];
  };

# -----------------------------------------
# Security Placeholders
# -----------------------------------------

  # AppArmor or SELinux - not enabled yet
  # security.apparmor.enable = true;
  # security.selinux.enable = true;

  # Fail2ban - not enabled yet
  # services.fail2ban.enable = true;

  # Yubikey integration placeholder
  # security.pam.u2f.enable = true;

  # System auditing beyond auditd
  # Further configurations can go here

  # DNS over HTTPS/TLS placeholder
  # services.dnscrypt-proxy2.enable = true;

# -----------------------------------------
# User Accounts
# -----------------------------------------

  users.users.alma = {
    isNormalUser = true;
    description = "Main Alma User";
    extraGroups = [ "wheel" "networkmanager" ];
    home = "/alma";
    shell = pkgs.zsh;
    initialPassword = "umamia";
  };

# -----------------------------------------
# Environment Packages
# -----------------------------------------

  environment.systemPackages = with pkgs; [
    vim
    git
    python3
    tree
    zip
    unzip
    p7zip
    gnupg
    age
    curl
    htop
    parted
    btrfs-progs
    cryptsetup
    vscode
    # Any other tools you might want to add
  ];

# -----------------------------------------
# Services
# -----------------------------------------

  # OpenSSH installed but disabled by default
  services.openssh = {
    enable = true;
    startWhenNeeded = false;
    settings.PermitRootLogin = "no";
    settings.PasswordAuthentication = true;
  };

  # Tailscale installed but disabled
  services.tailscale = {
    enable = true;
    useRoutingFeatures = "client";
    extraUpFlags = [];
    openFirewall = false;
  };

  # Auditd enabled for security auditing
  services.auditd.enable = true;

# -----------------------------------------
# Nix & Flakes
# -----------------------------------------

  nix = {
    package = pkgs.nixFlakes;
    extraOptions = ''
      experimental-features = nix-command flakes
    '';
  };

# -----------------------------------------
# System Version
# -----------------------------------------

  system.stateVersion = "23.11";

}

