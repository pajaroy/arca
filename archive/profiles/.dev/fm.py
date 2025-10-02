# ---
# version: "0.1.0"
# linked_to: "fm_v0.1.0.md"
# ---
# fm.py
from pathlib import Path
from datetime import date
import shutil
import csv
import argparse
from config import config  # tu config.py

class FileManager:
    def __init__(self, config):
        self.config = config
        self.INDEX = self.config.INDEX  # toma la ruta declarada en config.py
        self.INDEX.parent.mkdir(parents=True, exist_ok=True)  # aseguramos que la carpeta exista
        self._ensure_index()

    # Inicializa CSV si no existe
    def _ensure_index(self):
        if not self.INDEX.exists():
            with open(self.INDEX, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "path", "extension", "type", "date_created", "status"])

    # Actualiza CSV con nueva entrada
    def _add_to_index(self, path: Path, file_type: str):
        with open(self.INDEX, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                path.stem,
                str(path),
                path.suffix,
                file_type,
                date.today(),
                "active"
            ])

    # Crear archivo con carpeta contenedora
    def create_file(self, name: str, extension: str = ".py", file_type: str = "script", location: Path = None):
        if location is None:
            location = self.config.SRC

        folder_path = location / name
        folder_path.mkdir(parents=True, exist_ok=True)

        file_path = folder_path / f"{name}{extension}"

        # Metadatos iniciales
        metadatos = {
            "type": file_type,
            "date": str(date.today()),
            "version": self.config.__version__,
            "description": "",
            "linked_to": str(location),
            "changelog": "Inicial"
        }

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# ---\n")
            for key, val in metadatos.items():
                f.write(f"# {key}: {val}\n")
            f.write("# ---\n\n")

        self._add_to_index(file_path, file_type)
        print(f"Archivo creado en: {file_path}")
        return file_path

    # Borrar archivo o carpeta
    def delete_file(self, path: Path):
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"Eliminado: {path}")
            self._update_index_status(path, "deleted")
        else:
            print(f"No existe: {path}")

    # Mover archivo a otro lugar
    def move_file(self, path: Path, destination: Path):
        if path.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(destination))
            print(f"Movido: {path} -> {destination}")
            self._update_index_path(path, destination)
        else:
            print(f"No existe: {path}")

    # Listar archivos por extensión opcional
    def list_files(self, extension: str = None):
        with open(self.INDEX, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if extension is None or row["extension"] == extension:
                    print(row)

    # Actualiza status en el CSV
    def _update_index_status(self, path: Path, status: str):
        rows = []
        with open(self.INDEX, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        with open(self.INDEX, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                if row["path"] == str(path):
                    row["status"] = status
                writer.writerow(row)

    # Actualiza path en el CSV
    def _update_index_path(self, old_path: Path, new_path: Path):
        rows = []
        with open(self.INDEX, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        with open(self.INDEX, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                if row["path"] == str(old_path):
                    row["path"] = str(new_path)
                writer.writerow(row)

# ---- CLI ----
if __name__ == "__main__":
    fm = FileManager(config)

    parser = argparse.ArgumentParser(description="Gestor de archivos del proyecto")
    subparsers = parser.add_subparsers(dest="command")

    # Crear
    crear = subparsers.add_parser("crear")
    crear.add_argument("name")
    crear.add_argument("file_type", choices=["script", "doc"])
    crear.add_argument("extension")
    crear.add_argument("--location", default="src")

    # Borrar
    borrar = subparsers.add_parser("borrar")
    borrar.add_argument("path")

    # Mover
    mover = subparsers.add_parser("mover")
    mover.add_argument("path")
    mover.add_argument("destination")

    # Listar
    listar = subparsers.add_parser("listar")
    listar.add_argument("--ext", default=None)

    args = parser.parse_args()

    # Mapear location
    location_map = {
        "src": config.SRC,
        "doc": config.DOC,
        "data": config.DATA
    }

    if args.command == "crear":
        loc = location_map.get(args.location, config.SRC)
        fm.create_file(args.name, args.extension, args.file_type, loc)
    elif args.command == "borrar":
        fm.delete_file(Path(args.path))
    elif args.command == "mover":
        fm.move_file(Path(args.path), Path(args.destination))
    elif args.command == "listar":
        fm.list_files(args.ext)
