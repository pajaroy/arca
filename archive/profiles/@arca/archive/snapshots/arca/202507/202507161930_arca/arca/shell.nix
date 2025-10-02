{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.scikit-learn
    pkgs.python3Packages.pyyaml
  ];
}