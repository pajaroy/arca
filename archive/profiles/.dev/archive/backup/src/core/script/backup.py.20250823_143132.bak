# ---
# type: script
# date: 2025-08-22
# version: 0.1.0
# description: "Sistema de backup con historial de versiones"
# linked_to: /home/arca/trece/.dev/src
# changelog: Inicial
# ---
#!/usr/bin/env python3

import sys
from pathlib import Path
from datetime import datetime
import shutil
import argparse

# --- Ajustar path para importar config.py ---
sys.path.append(str(Path(__file__).resolve().parents[3]))  # sube hasta ~/trece/.dev
from config.config import config

class BackupSystem:
    def __init__(self):
        self.BACKUP = config.BACKUP
        self.BACKUP.mkdir(parents=True, exist_ok=True)
        self.max_backups = 10

    def _get_backup_dir(self, file_path: Path) -> Path:
        """Directorio de backup para un archivo específico"""
        try:
            relative_path = file_path.relative_to(config.ROOT)
        except ValueError:
            relative_path = Path(file_path.name)
        backup_dir = self.BACKUP / relative_path.parent
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir

    def _get_backup_files(self, file_path: Path):
        backup_dir = self._get_backup_dir(file_path)
        pattern = f"{file_path.name}.*.bak"
        return sorted(backup_dir.glob(pattern))

    def _clean_old_backups(self, backup_files):
        if len(backup_files) > self.max_backups:
            for old_file in backup_files[:-self.max_backups]:
                old_file.unlink()

    def create_backup(self, file_path: Path):
        if not file_path.exists() or not file_path.is_file():
            print(f"Error: {file_path} no existe o no es un archivo regular")
            return False

        backup_dir = self._get_backup_dir(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.bak"
        backup_path = backup_dir / backup_name

        try:
            shutil.copy2(file_path, backup_path)
            print(f"Backup creado: {backup_path}")
            backup_files = self._get_backup_files(file_path)
            self._clean_old_backups(backup_files)
            return True
        except Exception as e:
            print(f"Error creando backup: {e}")
            return False

    def list_backups(self, file_path: Path):
        backup_files = self._get_backup_files(file_path)
        if not backup_files:
            print(f"No hay backups para {file_path}")
            return
        print(f"Backups disponibles para {file_path}:")
        for i, backup_file in enumerate(backup_files, 1):
            timestamp = backup_file.name.split('.')[-2]
            size = backup_file.stat().st_size
            print(f"  {i}. {timestamp} - {size} bytes")

    def restore_backup(self, file_path: Path, backup_index: int = None):
        backup_files = self._get_backup_files(file_path)
        if not backup_files:
            print(f"No hay backups disponibles para {file_path}")
            return False
        if backup_index is None:
            backup_to_restore = backup_files[-1]
        else:
            try:
                backup_to_restore = backup_files[backup_index - 1]
            except IndexError:
                print(f"Índice inválido. Máximo: {len(backup_files)}")
                return False

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_to_restore, file_path)
            print(f"Backup restaurado: {backup_to_restore} -> {file_path}")
            return True
        except Exception as e:
            print(f"Error restaurando backup: {e}")
            return False

# ---------------- CLI ----------------
def main():
    parser = argparse.ArgumentParser(description="Sistema de backup con historial de versiones")
    parser.add_argument("action", choices=["backup", "restore", "list"], help="Acción a realizar")
    parser.add_argument("file", nargs="?", help="Ruta del archivo (relativa o absoluta)")
    parser.add_argument("--index", type=int, help="Índice del backup a restaurar (restore)")
    args = parser.parse_args()

    bs = BackupSystem()

    if not args.file:
        print("Error: Se requiere especificar un archivo")
        return

    file_path = Path(args.file).expanduser().absolute()

    if args.action == "backup":
        bs.create_backup(file_path)
    elif args.action == "list":
        bs.list_backups(file_path)
    elif args.action == "restore":
        bs.restore_backup(file_path, args.index)

if __name__ == "__main__":
    main()
