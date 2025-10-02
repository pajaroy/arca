import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.cmd.crear.crear_archivo import generar_frontmatter, crear_archivo
from utils.load_config.load_config import load_config
from utils.load_schema.load_schema import load_schema
from utils.hash_utils.hash_utils import hash_file
from ruamel.yaml import YAML

config = load_config()
schemas = load_schema()
base_path = Path(config["paths"]["base"])
schema_yaml = schemas["frontmatter"]

nombre = "README3"
tipo = "yaml"
autor = "Bird"

# Generar frontmatter dict
frontmatter = generar_frontmatter(schema_yaml, tipo, nombre, autor)

# Serializar frontmatter a YAML string
yaml = YAML()
from io import StringIO
s = StringIO()
yaml.dump(frontmatter, s)
frontmatter_str = s.getvalue()

# Contenido real del archivo
contenido_usuario = "descripcion: Archivo generado para pruebas de file_manager.\n"

# Mezclar encabezado YAML y contenido
contenido_final = f"{frontmatter_str}\n{contenido_usuario}"

# Crear archivo físico usando file_manager (esto también indexa y loguea)
crear_archivo(nombre, contenido_final, tipo, autor, destino=base_path)
