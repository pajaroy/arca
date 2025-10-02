{
  description = "ALMA_RESIST System flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      nixosConfigurations."alma-resist" = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [
          ./hardware-configuration.nix
          ./configuration.nix
        ];
      };
    };
}

