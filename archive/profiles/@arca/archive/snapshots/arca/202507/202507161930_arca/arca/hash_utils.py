"""METADATOS\nuuid: 7fc291ff-97b6-4c39-a820-4ccaef8153ea
tipo: py
nombre: hash_utils
version: 0.1.0
estado: activo
fecha_creacion: '2025-07-16T02:27:13.241794'
fecha_modificacion: '2025-07-16T02:27:13.241847'
autor: Bird
descripcion: Calculador de Hash universal
hash_integridad: ed9bf23b9e760a9fcb3f325a53c9ac5068f2b135dd8a4a6056220397d2cb04b8
\n"""

import hashlib

def calc_hash_file(filepath, algorithm="sha256"):
    """Calcula el hash de un archivo. Devuelve el string del hash."""
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def calc_hash_string(data, algorithm="sha256"):
    """Calcula el hash de un string (o bytes)."""
    if isinstance(data, str):
        data = data.encode()
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()
