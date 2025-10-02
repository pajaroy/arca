alias clear_empty='find ~/trece/.dev -type d -empty -delete'
alias clear_cache='find ~/trece/.dev -type d -name "__pycache__" -exec rm -rf {} +'

alias cli_versionar='python3 src/core/script/versionado.py versionar'
alias cli_backup='python3 src/core/script/backup.py backup'
alias cli_backup_restore='python3 src/core/script/backup.py restore'

alias create_prompt_dir='mkdir -p ~/trece/.dev/doc/prompt'
alias create_prompt='cp ~/trece/.dev/templates/prompt.md ~/trece/.dev/doc/prompt/'
