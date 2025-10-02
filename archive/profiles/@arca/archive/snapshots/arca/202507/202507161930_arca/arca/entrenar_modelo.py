"""METADATOS\nuuid: c03fda21-5c63-4db2-9ecf-554ee96b88da
tipo: py
nombre: entrenar_modelo
version: 0.1.0
estado: activo
fecha_creacion: '2025-07-16T00:34:31.445965'
fecha_modificacion: '2025-07-16T00:34:31.446020'
autor: Bird
descripcion: Entrena un modelo ML, lo guarda y crea metadatos con trazabilidad.
hash_integridad: 1e3bee2ca4f37f22462f5357e41abb7b79cb02ff3e1259bcfdb612ade3d8b285
\n"""
from load_config import load_config
from load_schema import load_schema
from hash_utils import calc_hash_file
from indexar_entrada import indexar_archivo
import pickle
import uuid
from datetime import datetime
from pathlib import Path
import yaml
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

CONFIG = load_config()
SCHEMA = load_schema()
MODELS_PATH = Path(CONFIG["config"]["models_path"])
MODELS_PATH.mkdir(exist_ok=True)
INDEX_INFO_TEMPLATE = CONFIG["config"]["index_info"]

def generar_frontmatter(campos_schema, args={}):
    frontmatter = {}
    for campo, default in campos_schema.items():
        if campo == "uuid":
            frontmatter[campo] = str(uuid.uuid4())
        elif campo in ["fecha_creacion", "fecha_modificacion"]:
            frontmatter[campo] = datetime.now().isoformat()
        elif campo == "hash_integridad":
            frontmatter[campo] = ""
        elif campo in args:
            frontmatter[campo] = args[campo]
        else:
            frontmatter[campo] = default
    return frontmatter

def validate_frontmatter(frontmatter, schema):
    for field in schema['metadatos_frontmatter'].keys():
        if field not in frontmatter:
            raise ValueError(f"Campo requerido faltante: {field}")
    return True

def save_model_with_metadata(model, model_name, **kwargs):
    model_file = MODELS_PATH / f"{model_name}.pkl"
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)

    campos_schema = SCHEMA['metadatos_frontmatter']
    args = {"tipo": "modelo", "nombre": model_file.name}
    args.update(kwargs)
    frontmatter = generar_frontmatter(campos_schema, args)
    validate_frontmatter(frontmatter, SCHEMA)

    # Calcula hash del modelo guardado
    hash_val = calc_hash_file(model_file)
    frontmatter["hash_integridad"] = hash_val

    # Guarda metadatos
    meta_file = MODELS_PATH / f"{model_name}.meta.yaml"
    with open(meta_file, "w") as f:
        yaml.dump(frontmatter, f, sort_keys=False)

    print(f"Modelo guardado: {model_file}")
    print(f"Metadatos guardados: {meta_file}")

    # Indexa el modelo usando la plantilla de config
    index_info = dict(INDEX_INFO_TEMPLATE)  # Copia
    index_info.update({
        "uuid": frontmatter.get("uuid"),
        "nombre": model_name,
        "ruta": str(model_file),
        "tipo": "modelo",
        "hash_integridad": hash_val,
        "fecha_creacion": frontmatter.get("fecha_creacion"),
        "fecha_modificacion": frontmatter.get("fecha_modificacion"),
        "autor": frontmatter.get("autor"),
        "descripcion": frontmatter.get("descripcion"),
    })
    indexar_archivo(index_info)

if __name__ == "__main__":
    # Entrenamiento DEMO (podés adaptar esto a tu CLI)
    iris = load_iris()
    X, y = iris.data, iris.target
    model = RandomForestClassifier().fit(X, y)
    save_model_with_metadata(
        model, "modelo_iris_rf",
        autor="Bird",
        descripcion="Modelo RF simple con iris"
    )
