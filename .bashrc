# ~/.arca/.bashrc
#opinion empower extend magic rookie notable master unlock knife doll current able
# PajaroDominic2025$

alias ll='ls -alF'
alias py='python3'
export PYTHONPATH=/arca/src
alias t='tree -I archive'
alias mk='mkdir -p'
alias c='clear'
alias rmpycache='find /arca -type d -name "__pycache__" -exec rm -rf {} +'

# Comandos Utiles

# Comandos para iniciar docker

# Construir docker: docker build -t [proyecto] .

# Modo persistente : sudo docker run -it -v $(pwd):/[app] --name [proyecto] [imagen] bash

# listar dockers: docker ps -a

# reutilizar docker: sudo docker start -ai [proyecto]

# Modo laboratorio: 

## sudo docker run -it --rm arca bash

## docker run --name arca-dev-test -it --rm arca-dev bash


# Comandos ollama
alias phi3='ollama run phi3'