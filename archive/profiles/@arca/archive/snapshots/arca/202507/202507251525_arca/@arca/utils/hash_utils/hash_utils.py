# utils/hash_utils.py

from blake3 import blake3
from pathlib import Path

def hash_string(data: str) -> str:
    """
    Calcula el hash BLAKE3 de un string.
    """
    return blake3(data.encode("utf-8")).hexdigest()

def hash_file(path: Path) -> str:
    """
    Calcula el hash BLAKE3 de un archivo.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")

    hasher = blake3()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
