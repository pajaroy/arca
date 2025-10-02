# Carga el .bashrc principal del usuario
if [ -f "$HOME/.bashrc" ]; then
    . "$HOME/.bashrc"
fi

# Carga automática de .bashrc locales al entrar en directorios
cd() {
    builtin cd "$@" || return
    if [ -f ".bashrc" ]; then
        . ".bashrc"  # Carga el .bashrc local relativo al directorio
    fi
}