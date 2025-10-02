{ pkgs ? import <nixpkgs> {} }:

let
  # Paquetes Python agrupados para mejor organización
  python-with-packages = pkgs.python3.withPackages (ps: with ps; [
    pandas
    nltk
    scikit-learn
    spacy
    pyyaml
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
    loguru
    rich
    # chromadb → se instalará por pip en el shellHook
    python-magic
    filetype
  ]);

  # Modelo de lenguaje español para spaCy
  spacy-model = pkgs.python3Packages.spacy-models.es_core_news_sm.overrideAttrs (oldAttrs: {
    version = "3.7.0";
  });

in pkgs.mkShell {
  buildInputs = [
    # Herramientas del sistema
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
    pkgs.libreoffice
    pkgs.exiftool
    pkgs.file            # necesario para python-magic
    pkgs.which

    # Herramientas para CSV/Datos (agregar en buildInputs)
    pkgs.csvkit
    pkgs.jq
    pkgs.miller
    pkgs.visidata
    # pkgs.python3Packages.q  # Para SQL sobre CSV

    # Requisitos de compilación para chromadb
    pkgs.gcc
    pkgs.cmake
    pkgs.python3Packages.setuptools
    pkgs.python3Packages.wheel

    # Entorno Python
    python-with-packages
    spacy-model
  ];

  shellHook = ''
    # Configuración del modelo spaCy
    export SPACY_DATA_DIR="${spacy-model}"
    mkdir -p $HOME/.local/share
    ln -sfn ${spacy-model} $HOME/.local/share/spacy

    # Verificación e instalación de chromadb
    if ! python -c "import chromadb" &>/dev/null; then
      echo "⚙️  Instalando chromadb vía pip..."
      pip install --no-cache-dir chromadb
    fi

    # Mensaje de confirmación
    echo ""
    echo "╔════════════════════════════════════╗"
    echo "║    Entorno configurado correcto    ║"
    echo "╠════════════════════════════════════╣"
    echo "║ • Python: $(python3 --version | cut -d' ' -f2)  ║"
    echo "║ • Pandas: $(python3 -c "import pandas; print(pandas.__version__)")       ║"
    echo "║ • spaCy: $(python3 -c "import spacy; print(spacy.__version__)")        ║"
    echo "╚════════════════════════════════════╝"
    echo ""
    echo "Modelo español disponible como: es_core_news_sm"
    echo ""
  '';
}
