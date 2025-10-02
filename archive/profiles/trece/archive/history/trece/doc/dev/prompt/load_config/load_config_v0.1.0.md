---
type: "prompt"
fecha: "2025-08-19"
version: "0.1.0"
descripcion: "pedido para script qe cargue config yaml"
---

# Prompt:

Quiero qe me pases un prompt para crear dos script, uno seria `~/trece/src/core/load_config.py` qe carga la configuracion yaml desde `~/trece/config/config.yaml` y que se exportable.
Estoy trabajando con pyproyect.toml

## Te dejo la config yaml a utilizar.

```yaml
# ~/trece/config/config.yaml

paths:
  archive:
    active: "archive/active"
    backup: "archive/backup"
    exports: "archive/exports"
    history: "archive/history"
  database: "database/trece.db"
  meta:
    schema_sql: "meta/schema.sql"
    schema_yaml: "meta/schema.yaml"
  src:
    core: "src/core"
    scripts: "src/script"   # <- corregido plural (si aplica)
    utils: "src/util"       # <- corregido plural (si aplica)
  templates: "templates"
  tmp: "tmp"

settings:
  default_template: "template_flujo_interno_beta.csv"
  # db_connection lo podés generar en el código a partir de paths.database
```

Y el segundo script seria un test para verificar que cargo bien la config.yaml