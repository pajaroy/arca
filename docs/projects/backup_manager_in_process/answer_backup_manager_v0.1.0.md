---
type: "answer"
version: "0.1.0"
description: "Respuesta a prompt_backup_manager_v0.1.0.md
linked_to: prompt_backup_manager_v0.1.0.md y backup_manager.py

---
Perfecto, voy a reestructurar el script según tu nueva configuración. Aquí está la implementación actualizada:

## 📁 Archivos actualizados

### 1. `config.yaml` (actualizado)

```yaml
version: "0.2.0"
author: "bird"

root: /arca

paths:
  archive: /arca/archive
  backup: /arca/archive/backup
  history: /arca/archive/history

meta:
  supported_extensions:
    - .yaml
    - .yml
    - .md
    - .json
    - .py
    - .csv

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  date_format: "%Y-%m-%d %H:%M:%S"
```

### 2. `main.py` (completamente actualizado)

```python
#!/usr/bin/env python3
"""
Backup Manager 0.1.0
Sistema de gestión de copias de seguridad para el ecosistema ARCA
"""

import argparse
import logging
import json
import tarfile
from datetime import datetime
from pathlib import Path
import yaml
import sys


class BackupManager:
    def __init__(self, config_path: Path = Path("/arca/src/core/manager/config.yaml")):
        """Inicializa el Backup Manager con la configuración proporcionada."""
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Configurar rutas usando pathlib
        self.root_path = Path(self.config['root'])
        self.backup_path = Path(self.config['paths']['backup'])
        self.archive_path = Path(self.config['paths']['archive'])
        self.history_path = Path(self.config['paths']['history'])
        
        # Crear directorios necesarios
        self.backup_path.mkdir(parents=True, exist_ok=True)
        self.history_path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("Backup Manager inicializado")

    def _load_config(self, config_path: Path) -> dict:
        """Carga la configuración desde el archivo YAML."""
        try:
            with config_path.open('r') as f:
                config = yaml.safe_load(f)
            
            # Validar configuración mínima requerida
            required_keys = ['root', 'paths.backup', 'paths.archive', 'paths.history']
            for key in required_keys:
                keys = key.split('.')
                current = config
                for k in keys:
                    if k not in current:
                        raise ValueError(f"Configuración requerida faltante: {key}")
                    current = current[k]
            
            return config
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            sys.exit(1)

    def _setup_logging(self):
        """Configura el sistema de logging."""
        logging_config = self.config.get('logging', {})
        
        logging.basicConfig(
            level=getattr(logging, logging_config.get('level', 'INFO')),
            format=logging_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            datefmt=logging_config.get('date_format', '%Y-%m-%d %H:%M:%S'),
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(self.history_path / 'backup_manager.log')
            ]
        )

    def _get_relative_path(self, absolute_path: Path) -> Path:
        """Convierte una ruta absoluta a relativa dentro del root."""
        try:
            return absolute_path.relative_to(self.root_path)
        except ValueError:
            # Si la ruta no está dentro del root, devolverla completa pero como relativa
            return Path(absolute_path.name)

    def _get_backup_filename(self, source_path: Path, description: str = None) -> str:
        """Genera el nombre del archivo de backup."""
        relative_path = self._get_relative_path(source_path)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Crear nombre seguro para el archivo
        safe_name = str(relative_path).replace('/', '_').replace('\\', '_')
        
        if description:
            safe_desc = description.replace(' ', '_').replace('/', '_')
            filename = f"{safe_name}_{safe_desc}_{timestamp}.tar.gz"
        else:
            filename = f"{safe_name}_{timestamp}.tar.gz"
        
        return filename

    def _get_backup_filepath(self, source_path: Path, description: str = None) -> Path:
        """Genera la ruta completa del archivo de backup."""
        relative_path = self._get_relative_path(source_path)
        backup_dir = self.backup_path / relative_path.parent
        filename = self._get_backup_filename(source_path, description)
        
        return backup_dir / filename

    def _should_include_file(self, file_path: Path) -> bool:
        """Determina si un archivo debe ser incluido en el backup basado en extensiones soportadas."""
        supported_extensions = self.config['meta']['supported_extensions']
        return file_path.suffix.lower() in supported_extensions

    def _filter_files_for_backup(self, source_path: Path) -> list:
        """Filtra archivos basado en las extensiones soportadas."""
        if source_path.is_file():
            return [source_path] if self._should_include_file(source_path) else []
        
        files_to_backup = []
        for file_path in source_path.rglob('*'):
            if file_path.is_file() and self._should_include_file(file_path):
                files_to_backup.append(file_path)
        
        return files_to_backup

    def _cleanup_old_backups(self, source_path: Path, max_backups: int):
        """Elimina backups antiguos excediendo el máximo permitido."""
        relative_path = self._get_relative_path(source_path)
        backup_dir = self.backup_path / relative_path.parent
        
        if not backup_dir.exists():
            return
        
        # Patrón para identificar backups del mismo archivo/directorio
        base_pattern = str(relative_path).replace('/', '_').replace('\\', '_')
        
        backups = []
        for backup_file in backup_dir.glob(f"{base_pattern}*.tar.gz"):
            if backup_file.is_file():
                backups.append((backup_file, backup_file.stat().st_ctime))
        
        # Ordenar por fecha de creación (más antiguo primero)
        backups.sort(key=lambda x: x[1])
        
        # Eliminar backups excedentes
        while len(backups) > max_backups:
            oldest_backup = backups.pop(0)
            try:
                oldest_backup[0].unlink()
                self.logger.info(f"Eliminado backup antiguo: {oldest_backup[0]}")
            except Exception as e:
                self.logger.error(f"Error eliminando backup {oldest_backup[0]}: {e}")

    def create_backup(self, source_path: Path, description: str = None, max_backups: int = 5) -> bool:
        """Crea un backup del archivo o directorio especificado."""
        source_path = Path(source_path)
        
        if not source_path.exists():
            self.logger.error(f"La ruta fuente no existe: {source_path}")
            return False

        files_to_backup = self._filter_files_for_backup(source_path)
        if not files_to_backup:
            self.logger.warning(f"No se encontraron archivos con extensiones soportadas en: {source_path}")
            return False

        backup_filepath = self._get_backup_filepath(source_path, description)
        
        try:
            # Crear directorio de backup si no existe
            backup_filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Crear archivo tar.gz
            with tarfile.open(backup_filepath, "w:gz") as tar:
                for file_path in files_to_backup:
                    arcname = self._get_relative_path(file_path)
                    tar.add(file_path, arcname=str(arcname))
            
            self.logger.info(f"Backup creado exitosamente: {backup_filepath}")
            self.logger.info(f"Archivos incluidos: {len(files_to_backup)}")
            
            # Limpiar backups antiguos
            self._cleanup_old_backups(source_path, max_backups)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creando backup: {e}")
            return False

    def list_backups(self, json_output: bool = False):
        """Lista todos los backups disponibles."""
        if not self.backup_path.exists():
            if json_output:
                print(json.dumps([]))
            else:
                print("No hay backups disponibles.")
            return

        backups = []
        
        for backup_file in self.backup_path.rglob("*.tar.gz"):
            if backup_file.is_file():
                stat = backup_file.stat()
                
                # Extraer información del nombre del archivo
                filename_parts = backup_file.stem.split('_')  # Remover .tar.gz
                
                # Reconstruir ruta original
                relative_backup_dir = backup_file.parent.relative_to(self.backup_path)
                original_path = self.root_path / relative_backup_dir
                
                backup_info = {
                    'backup_path': str(backup_file),
                    'original_path': str(original_path),
                    'filename': backup_file.name,
                    'size_bytes': stat.st_size,
                    'size_human': f"{stat.st_size / 1024 / 1024:.1f} MB",
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'created_human': datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                    'description': None
                }
                
                # Intentar extraer descripción si existe
                if len(filename_parts) > 2:
                    # La descripción está entre el nombre base y el timestamp
                    base_name_parts = str(relative_backup_dir).split('/')
                    base_name = base_name_parts[-1] if base_name_parts else filename_parts[0]
                    
                    if base_name in filename_parts:
                        desc_index = filename_parts.index(base_name) + 1
                        if desc_index < len(filename_parts) - 1:  # Verificar que no sea el timestamp
                            backup_info['description'] = filename_parts[desc_index]
                
                backups.append(backup_info)
        
        if json_output:
            print(json.dumps(backups, indent=2))
        else:
            if not backups:
                print("No hay backups disponibles.")
                return
            
            print(f"{'Archivo':<40} {'Ruta Original':<30} {'Tamaño':<10} {'Fecha':<20} {'Descripción'}")
            print("-" * 120)
            for backup in backups:
                desc = backup['description'] or ""
                print(f"{backup['filename']:<40} {Path(backup['original_path']).name:<30} "
                      f"{backup['size_human']:<10} {backup['created_human']:<20} {desc}")

    def restore_backup(self, backup_path: Path, target_path: Path = None, force: bool = False) -> bool:
        """Restaura un backup a su ubicación original o a una ruta alternativa."""
        backup_path = Path(backup_path)
        
        if not backup_path.exists():
            self.logger.error(f"El archivo de backup no existe: {backup_path}")
            return False

        # Determinar ruta de destino
        if target_path is None:
            # Extraer ruta original del directorio del backup
            relative_backup_dir = backup_path.parent.relative_to(self.backup_path)
            target_path = self.root_path / relative_backup_dir
        else:
            target_path = Path(target_path)

        # Verificar si el destino ya existe
        if target_path.exists() and not force:
            response = input(f"El destino {target_path} ya existe. ¿Sobrescribir? (y/N): ")
            if response.lower() != 'y':
                self.logger.info("Restauración cancelada por el usuario")
                return False
            else:
                self.logger.warning(f"Sobrescribiendo contenido en: {target_path}")

        try:
            # Crear directorio de destino si no existe
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Extraer backup
            with tarfile.open(backup_path, "r:gz") as tar:
                tar.extractall(target_path)
            
            self.logger.info(f"Backup restaurado exitosamente: {backup_path} -> {target_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error restaurando backup: {e}")
            return False


def main():
    """Función principal del CLI."""
    parser = argparse.ArgumentParser(description="Backup Manager 0.1.0")
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando create
    create_parser = subparsers.add_parser('create', help='Crear un nuevo backup')
    create_parser.add_argument('source', help='Ruta del archivo o directorio a respaldar')
    create_parser.add_argument('--desc', help='Descripción del backup')
    create_parser.add_argument('--max', type=int, default=5, help='Número máximo de backups a mantener (default: 5)')
    
    # Comando list
    list_parser = subparsers.add_parser('list', help='Listar backups disponibles')
    list_parser.add_argument('--json', action='store_true', help='Salida en formato JSON')
    
    # Comando restore
    restore_parser = subparsers.add_parser('restore', help='Restaurar un backup')
    restore_parser.add_argument('backup_path', help='Ruta del archivo de backup a restaurar')
    restore_parser.add_argument('--target', help='Ruta alternativa de destino')
    restore_parser.add_argument('--force', action='store_true', help='Forzar sobrescritura sin confirmación')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Inicializar manager
    manager = BackupManager()
    
    try:
        if args.command == 'create':
            success = manager.create_backup(
                Path(args.source), 
                args.desc, 
                args.max
            )
            if not success:
                sys.exit(1)
                
        elif args.command == 'list':
            manager.list_backups(args.json)
            
        elif args.command == 'restore':
            target_path = Path(args.target) if args.target else None
            success = manager.restore_backup(
                Path(args.backup_path), 
                target_path, 
                args.force
            )
            if not success:
                sys.exit(1)
                
    except KeyboardInterrupt:
        manager.logger.info("Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        manager.logger.error(f"Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 3. `README.md` (actualizado)

```markdown
# Backup Manager 0.1.0

Sistema de gestión de copias de seguridad para el ecosistema ARCA.

## Características

- ✅ Creación de backups comprimidos (.tar.gz) usando `tarfile`
- ✅ Filtrado por extensiones soportadas (configurable en `config.yaml`)
- ✅ Listado de backups con metadatos
- ✅ Restauración de backups con confirmación de seguridad
- ✅ Rotación automática de backups
- ✅ Configuración flexible via YAML
- ✅ Logging centralizado con `logging.getLogger(__name__)`
- ✅ Manejo de rutas con `pathlib`

## Uso

### Crear backup
```bash
python3 main.py create /arca/src/data --desc "Backup inicial" --max 5
```

### Listar backups
```bash
python3 main.py list
python3 main.py list --json
```

### Restaurar backup
```bash
python3 main.py restore /arca/archive/backup/src/data/file_2025-09-24_01-00-00.tar.gz
python3 main.py restore backup.tar.gz --target /arca/tmp/restore --force
```

## Configuración

Editar `config.yaml` para modificar:

- **Rutas principales**: `root`, `paths.backup`, `paths.archive`, `paths.history`
- **Extensiones soportadas**: `meta.supported_extensions`
- **Logging**: nivel, formato y configuración

## Estructura de almacenamiento

Los backups se almacenan manteniendo la estructura original:
```
/arca/archive/backup/src/core/manager/main.py_2025-09-24_01-00-00.tar.gz
```

## Extensiones soportadas por defecto

- `.yaml`, `.yml` (configuraciones)
- `.md` (documentación)
- `.json` (datos)
- `.py` (código Python)
- `.csv` (datos tabulares)
```

## 🔄 Cambios principales realizados

1. **Uso de `pathlib`** para todas las operaciones de rutas
2. **Integración con la nueva `config.yaml`** con la estructura especificada
3. **Filtrado por extensiones** usando `meta.supported_extensions`
4. **Logging mejorado** con `logging.getLogger(__name__)`
5. **Manejo de rutas relativas** dentro del ecosistema ARCA
6. **Estructura de directorios** según `paths.backup`, `paths.archive`, `paths.history`

## 🚀 Pruebas rápidas

```bash
# Crear directorios necesarios
mkdir -p /arca/archive/backup /arca/archive/history

# Probar creación de backup
python3 main.py create /arca/src/core/manager --desc "prueba_backup" --max 3

# Listar backups
python3 main.py list

# Probar salida JSON
python3 main.py list --json
```

El script ahora está completamente integrado con tu nueva estructura de configuración y utiliza las librerías especificadas (`pathlib`, `logging`, etc.). ¿Te gustaría que ajuste algún aspecto específico?