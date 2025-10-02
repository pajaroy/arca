{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python311.withPackages (ps: with ps; [
    # Core
    pip
    pytest
    pytest-cov
    ipykernel
    
    # Data Processing
    numpy
    pandas
    pyarrow
    scikit-learn
    joblib
    
    # YAML/JSON
    pyyaml
    ruamel-yaml
    jsonschema
    
    # Web/API
    fastapi
    cryptography
    
    # CLI
    typer
    tabulate
    rich
    loguru
    
    # NLP
    nltk
    spacy
    
    # Jupyter
    notebook
    jupyterlab
  ]);

in pkgs.mkShell {
  name = "trece-dev-env";

  buildInputs = [
    # Python y herramientas esenciales
    pythonEnv
    pkgs.git
    pkgs.sqlite
    pkgs.gcc
  ];

  shellHook = ''
    # ----------------------------
    # 1. Configuración de Bash History (como solicitaste)
    # ----------------------------
    export HISTFILE="$PWD/.bash_history"
    touch "$HISTFILE"
    export HISTSIZE=100000
    export HISTFILESIZE=100000
    shopt -s histappend
    export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"
    
    # Carga .bashrc local si existe
    [ -f "$PWD/.bashrc" ] && source "$PWD/.bashrc"

    # ----------------------------
    # 2. Configuración de Python
    # ----------------------------
    export PYTHONPATH="$PWD/src:${pythonEnv}/${pythonEnv.sitePackages}"
    
    # ----------------------------
    # 3. Mensaje de inicio
    # ----------------------------
    echo ""
    echo "🐍 Entorno Python para trece activado"
    echo "📜 Historial de Bash guardado en: $PWD/.bash_history"
    echo ""
    echo "Herramientas disponibles:"
    echo "- Python ${pythonEnv.python.version}"
    echo "- Jupyter: ejecuta 'jupyter lab'"
    echo "- Para spaCy: descarga modelos con 'python -m spacy download es_core_news_sm'"
    echo ""
    echo "Directorio actual: $PWD"
  '';
}