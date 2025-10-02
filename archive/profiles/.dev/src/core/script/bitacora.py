# ---
# version: 0.1.0
# ---
# Ejemplo de uso: 
#  - python3 -m src.core.script.bitacora --resumen "Día de pruebas con plantillas en Python" --tags desarrollo organización
#
# src/core/bitacora.py
import sys
from pathlib import Path
import yaml
from datetime import date
import argparse
from config.config import config  # tu config central

class Bitacora:
    def __init__(self):
        self.config = config
        self.dir_bitacora = self.config.BITACORA
        self.dir_bitacora.mkdir(parents=True, exist_ok=True)

        # acá guardamos la entrada actual
        self.bitacora = {
            "fecha": str(date.today()),
            "autor": self.config.AUTOR,
            "resumen": "",
            "tags": []
        }

    def set_resumen(self, texto: str):
        self.bitacora["resumen"] = texto

    def set_tags(self, tags: list):
        self.bitacora["tags"] = tags

    def save(self, filename: str = None):
        if not filename:
            filename = f"{self.bitacora['fecha']}.yaml"

        out_path = self.dir_bitacora / filename
        with open(out_path, "w") as f:
            yaml.safe_dump(self.bitacora, f, sort_keys=False, allow_unicode=True)

        print(f"✅ Bitácora guardada en: {out_path}")
        return out_path


def main():
    parser = argparse.ArgumentParser(description="Registrar una bitácora diaria")
    parser.add_argument("--resumen", type=str, required=True, help="Resumen del día")
    parser.add_argument("--tags", nargs="*", default=[], help="Lista de tags")
    args = parser.parse_args()

    b = Bitacora()
    b.set_resumen(args.resumen)
    b.set_tags(args.tags)
    b.save()


if __name__ == "__main__":
    main()

