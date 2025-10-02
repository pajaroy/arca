# ---
# type: "script"
# fecha: "2025-08-20"
# version: "0.1.0"
# descripcion: "Script de ejemplo con versión"
# ---
#!/usr/bin/env python3

import os
import pathlib
import sys
import shutil
import yaml
from config.config import config

BASE_DIR = os.path.expanduser("~/arca")
HISTORY_DIR = os.path.join(BASE_DIR, "archive/history/arca")

SUPPORTED_EXTENSIONS = [".yaml", ".yml", ".md", ".json", ".py"]

def extract_yaml_version(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if lines[0].strip().lstrip("#").strip() != "---":
            return None

        yaml_lines = []
        for line in lines[1:]:
            clean_line = line.lstrip("#").strip()  # elimina "#" al inicio en .py
            if clean_line == "---":
                break
            yaml_lines.append(clean_line + "\n")

        yaml_content = yaml.safe_load("".join(yaml_lines))
        if isinstance(yaml_content, dict):
            return yaml_content.get("version")

    except Exception as e:
        print(f"Error leyendo encabezado YAML en {file_path}: {e}")
    return None

def get_relative_path(file_path):
    return os.path.relpath(file_path, BASE_DIR)

def version_file(file_path):
    if not os.path.isfile(file_path):
        print(f"No se encontró el archivo: {file_path}")
        return
    ext = os.path.splitext(file_path)[1]
    if ext not in SUPPORTED_EXTENSIONS:
        print(f"Archivo no soportado: {file_path}")
        return
    version = extract_yaml_version(file_path)
    if not version:
        print(f"Archivo sin versión en encabezado YAML: {file_path}")
        return
    rel_path = get_relative_path(file_path)
    target_dir = os.path.join(HISTORY_DIR, os.path.dirname(rel_path))
    os.makedirs(target_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    new_name = f"{base_name}_v{version}{ext}"
    target_path = os.path.join(target_dir, new_name)
    shutil.copy2(file_path, target_path)
    print(f"Archivo versionado: {target_path}")

def restore_file(versioned_file_path):
    if not os.path.isfile(versioned_file_path):
        print(f"No se encontró la versión: {versioned_file_path}")
        return
    rel_path = os.path.relpath(versioned_file_path, HISTORY_DIR)
    # Quitamos el sufijo _vX.X.X
    base_name, ext = os.path.splitext(os.path.basename(rel_path))
    if "_v" in base_name:
        base_name = base_name.split("_v")[0]
    original_rel_dir = os.path.dirname(rel_path)
    original_path = os.path.join(BASE_DIR, original_rel_dir, f"{base_name}{ext}")
    os.makedirs(os.path.dirname(original_path), exist_ok=True)
    shutil.copy2(versioned_file_path, original_path)
    print(f"Archivo restaurado: {original_path}")

def print_usage():
    print(f"Uso:\n"
          f"  {sys.argv[0]} versionar <archivo>\n"
          f"  {sys.argv[0]} restaurar <archivo_versionado>")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)
    action, file_path = sys.argv[1], sys.argv[2]
    if action == "versionar":
        version_file(os.path.abspath(file_path))
    elif action == "restaurar":
        restore_file(os.path.abspath(file_path))
    else:
        print_usage()
