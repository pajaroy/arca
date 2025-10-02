# ---
# type: "script"
# fecha: "2025-08-20"
# version: "0.1.0"
# descripcion: "Sistema de backup con historial de versiones"
# ---
#
# Mantiene hasta 10 backups por archivo en ~/trece/archive/backup/

#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path

class BackupSystem:
    def __init__(self):
        self.backup_base = Path.home() / "arca" / "archive" / "backup"
        self.backup_base.mkdir(parents=True, exist_ok=True)
        self.max_backups = 10

    def _get_backup_dir(self, file_path):
        """Obtiene el directorio de backup para un archivo específico"""
        relative_path = file_path.relative_to(Path.home())
        backup_dir = self.backup_base / relative_path.parent
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir

    def _get_backup_files(self, file_path):
        """Obtiene la lista de backups existentes para un archivo"""
        backup_dir = self._get_backup_dir(file_path)
        file_name = file_path.name
        pattern = f"{file_name}.*.bak"
        return sorted(backup_dir.glob(pattern))

    def _clean_old_backups(self, backup_files):
        """Elimina backups antiguos manteniendo solo los más recientes"""
        if len(backup_files) > self.max_backups:
            files_to_delete = backup_files[:-self.max_backups]
            for old_file in files_to_delete:
                old_file.unlink()

    def create_backup(self, file_path):
        """Crea un backup del archivo especificado"""
        if not file_path.exists():
            print(f"Error: El archivo {file_path} no existe")
            return False

        if not file_path.is_file():
            print(f"Error: {file_path} no es un archivo regular")
            return False

        # Crear directorio de backup si no existe
        backup_dir = self._get_backup_dir(file_path)
        
        # Generar nombre de backup con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.bak"
        backup_path = backup_dir / backup_name

        try:
            # Copiar el archivo
            shutil.copy2(file_path, backup_path)
            print(f"Backup creado: {backup_path}")

            # Limpiar backups antiguos
            backup_files = self._get_backup_files(file_path)
            self._clean_old_backups(backup_files)

            return True

        except Exception as e:
            print(f"Error creando backup: {e}")
            return False

    def list_backups(self, file_path):
        """Lista todos los backups disponibles para un archivo"""
        backup_files = self._get_backup_files(file_path)
        
        if not backup_files:
            print(f"No hay backups para {file_path}")
            return

        print(f"Backups disponibles para {file_path}:")
        for i, backup_file in enumerate(backup_files, 1):
            timestamp = backup_file.name.split('.')[-2]
            size = backup_file.stat().st_size
            print(f"  {i}. {timestamp} - {size} bytes")

    def restore_backup(self, file_path, backup_index=None):
        """Restaura el backup más reciente o uno específico"""
        backup_files = self._get_backup_files(file_path)
        
        if not backup_files:
            print(f"No hay backups disponibles para {file_path}")
            return False

        # Si no se especifica índice, usar el más reciente
        if backup_index is None:
            backup_to_restore = backup_files[-1]
        else:
            try:
                backup_to_restore = backup_files[backup_index - 1]
            except IndexError:
                print(f"Índice de backup inválido. Máximo: {len(backup_files)}")
                return False

        try:
            # Asegurar que el directorio destino existe
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Restaurar el backup
            shutil.copy2(backup_to_restore, file_path)
            print(f"Backup restaurado: {backup_to_restore} -> {file_path}")
            return True

        except Exception as e:
            print(f"Error restaurando backup: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Sistema de backup con historial de versiones")
    parser.add_argument("action", choices=["backup", "restore", "list"], 
                       help="Acción a realizar")
    parser.add_argument("file", nargs="?", 
                       help="Ruta del archivo (relativa o absoluta)")
    parser.add_argument("--index", type=int,
                       help="Índice del backup a restaurar (para acción 'restore')")

    args = parser.parse_args()
    backup_system = BackupSystem()

    if args.action == "backup":
        if not args.file:
            print("Error: Se requiere especificar un archivo para backup")
            sys.exit(1)
        
        file_path = Path(args.file).expanduser().absolute()
        if not backup_system.create_backup(file_path):
            sys.exit(1)

    elif args.action == "list":
        if not args.file:
            print("Error: Se requiere especificar un archivo para listar backups")
            sys.exit(1)
        
        file_path = Path(args.file).expanduser().absolute()
        backup_system.list_backups(file_path)

    elif args.action == "restore":
        if not args.file:
            print("Error: Se requiere especificar un archivo para restaurar")
            sys.exit(1)
        
        file_path = Path(args.file).expanduser().absolute()
        if not backup_system.restore_backup(file_path, args.index):
            sys.exit(1)

if __name__ == "__main__":
    main()