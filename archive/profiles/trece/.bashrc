# ~/trece/.bashrc

eval "$(direnv hook bash)"

# Carga el historial existente
if [ -f "$PWD/.bash_history" ]; then
    history -r "$PWD/.bash_history"
fi

export PROMPT_COMMAND='history -a; history -n; history -r'
shopt -s histappend
export HISTSIZE=100000
export HISTFILESIZE=200000
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"

#####################################################################################################

# Alias útiles (opcional)
alias l="ls -lah"
alias run="./script/start"  # Ejemplo para tu proyecto
alias actenv='source .venv/bin/activate'

# Backup y versionado
alias backup='python3 ~/trece/src/script/backup.py backup'
alias backup_restore='python3 ~/trece/src/script/backup.py restore'
alias versionar='python3 ~/trece/src/script/versionado.py versionar'        