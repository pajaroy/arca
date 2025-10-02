
{ config, lib, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
      ./modules/base.nix
      ./modules/xfce.nix
      ./modules/filesystems.nix
    ];

  system.stateVersion = "24.05"; # Did you read the comment?

}

