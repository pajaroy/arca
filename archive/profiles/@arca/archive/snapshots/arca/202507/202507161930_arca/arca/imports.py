"""METADATOS\nuuid: 3aa08a8a-c741-41b5-bba5-a7dace99e01b
tipo: py
nombre: imports
version: 0.1.0
estado: activo
fecha_creacion: '2025-07-16T01:38:26.770917'
fecha_modificacion: '2025-07-16T01:38:26.770968'
autor: Bird
descripcion: Imports Generales del sistema ARCA
hash_integridad: a8d78bde3fdc8c8711964f075c94592006facf66faf7cfe1e92ae1244b445db7
\n"""

# Importar load_config.py

from load_config import load_config
CONFIG = load_config()

# Importar load_schema.py

from load_schema import load_schema
SCHEMA = load_schema()

# Hash utis and index

from hash_utils import calc_hash_file
from indexar_entrada import indexar_archivo

# ...tu lógica...

# 1. Calcular hash del archivo
hash_val = calc_hash_file("ruta/al/archivo.ext")

# 2. Indexar
info = {
    "uuid": "...",
    "nombre": "...",
    "ruta": "ruta/al/archivo.ext",
    "hash_integridad": hash_val,
    # ...otros campos...
}
indexar_archivo(info)


# Importar arca_creator.py

from arca_creator import crear_archivo

## Ejemplo de uso :

crear_archivo("yaml", "mi_nuevo_modulo", autor="Bird", descripcion="Descripción demo")


# Importar entrenar_modelo.py

from entrenar_modelo import save_model_with_metadata

## Ejemplo de uso :

# Supongamos que ya entrenaste un modelo llamado "modelo"
save_model_with_metadata(modelo, "nombre_del_modelo", autor="Bird", descripcion="Un modelo entrenado")
