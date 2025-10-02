{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.tmux
    pkgs.vim
    pkgs.git
    pkgs.tree
    pkgs.htop
    pkgs.curl
    pkgs.wget
    pkgs.zip
    pkgs.unzip
    pkgs.p7zip
    pkgs.gnupg
    pkgs.age
    pkgs.nano
    pkgs.sqlite
    pkgs.ncdu
    pkgs.ranger
    pkgs.neofetch
    pkgs.btop
    pkgs.libreoffice   # si realmente la necesitás en desarrollo
    pkgs.python3
    (pkgs.python3.withPackages (ps: with ps; [
      pyyaml
      pandas
      pyarrow
      ruamel-yaml
      notebook
      jupyterlab
      ipykernel
      typer
      tabulate
      joblib
      pip
      jsonschema
      cryptography
      fastapi
      pytest
      numpy
      scikit-learn
      loguru
      rich
    ]))
  ];

  shellHook = ''
    [ -d .venv ] || python3 -m venv .venv
    source .venv/bin/activate
    echo "¡Entorno de desarrollo activado!"
  '';
}
