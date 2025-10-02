# 🧩 Apéndice – Backup automático a GitHub con `backup_to_git.sh`

## 📁 Ubicación del script
`/home/bird/ALMA_RESIST/core/scripts/backup_to_git/backup_to_git.sh`

## 📌 Requisitos

```bash
sudo apt install inotify-tools git
```

## 🛠️ Pasos de configuración

```bash
# 1. Configurar Git si aún no está hecho
git config --global user.name "bird"
git config --global user.email "distribuidorasolar365@gmail.com"

# 2. Verificar que ALMA_RESIST sea repositorio Git
cd ~/ALMA_RESIST
git init
git remote add origin git@github.com:pajaroy/alma_resist.git
git branch -M main
git pull origin main

# 3. Dar permisos y lanzar en segundo plano
chmod +x /home/bird/ALMA_RESIST/core/scripts/backup_to_git/backup_to_git.sh
nohup /home/bird/ALMA_RESIST/core/scripts/backup_to_git/backup_to_git.sh > /dev/null 2>&1 &
```

## 🔐 Clave SSH y autenticación

```bash
ssh-keygen -t ed25519 -C "distribuidorasolar365@gmail.com"
cat ~/.ssh/id_ed25519.pub  # Copiar a GitHub > Settings > SSH Keys
ssh -T git@github.com      # Verificar autenticación
```

## 🧠 Notas importantes

- Este script monitoriza cambios en tiempo real y los **sube automáticamente** a GitHub.
- Evita eliminar archivos directamente, ya que el sistema detectará conflictos. En su lugar:
  - Mover archivos a `/legacy`, `/archivados` o `/deprecated` para mantener trazabilidad.
- Logs ubicados en:
  - `/home/bird/ALMA_RESIST/logs/backup_git/backup_git.log`
- Si falla el push por cambios no comiteados:
  - Revisión manual: `git status`, `git stash`, `git commit -am`, etc.

## 🧼 Detener proceso en background si es necesario

```bash
pkill -f backup_to_git.sh
```
