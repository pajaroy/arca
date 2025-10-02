# utils/load_schema.py

from utils.load_config.load_config import load_config
from ruamel.yaml import YAML
from pathlib import Path

def load_schema() -> dict:
    """
    Carga todos los schemas YAML y SQL-schema (en YAML) definidos en config.yaml.
    """
    config = load_config()
    base = Path(config["paths"]["base"])
    yaml_dir = base / config["paths"]["schemas_yaml_dir"]
    sql_dir = base / config["paths"]["schemas_sql_dir"]

    yaml = YAML(typ="safe")
    schemas = {}

    # Schemas YAML clásicos
    for path in yaml_dir.glob("*.yaml"):
        with path.open("r", encoding="utf-8") as f:
            schemas[path.stem] = yaml.load(f)

    # Schemas SQL, extensión .sql
    for path in sql_dir.glob("*.sql"):
        with path.open("r", encoding="utf-8") as f:
            schemas[f"{path.stem}_sql"] = yaml.load(f)

    return schemas
