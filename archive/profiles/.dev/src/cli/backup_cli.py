#!/usr/bin/env python3
import argparse
from pathlib import Path
from config.config import config
from src.core.script.backup import BackupSystem

def main():
    parser = argparse.ArgumentParser(description="Sistema de backup con historial de versiones")
    parser.add_argument("action", choices=["backup", "restore", "list"], help="Acción a realizar")
    parser.add_argument("file", nargs="?", help="Ruta del archivo (relativa o absoluta)")
    parser.add_argument("--index", type=int, help="Índice del backup a restaurar (restore)")
    args = parser.parse_args()

    bs = BackupSystem()

    if not args.file:
        parser.error("Se requiere especificar un archivo")

    file_path = Path(args.file).expanduser().absolute()

    if args.action == "backup":
        backup_path = bs.create_backup(file_path)
        print(f"Backup creado: {backup_path}")

    elif args.action == "list":
        backups = bs.list_backups(file_path)
        if not backups:
            print(f"No hay backups para {file_path}")
        else:
            print(f"Backups disponibles para {file_path}:")
            for i, (bf, size) in enumerate(backups, 1):
                timestamp = bf.name.split('.')[-2]
                print(f"  {i}. {timestamp} - {size} bytes")

    elif args.action == "restore":
        restored = bs.restore_backup(file_path, args.index)
        print(f"Backup restaurado: {restored} -> {file_path}")

if __name__ == "__main__":
    main()
