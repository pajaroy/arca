---
version: "0.1.0"
linked_to: "fm_v0.1.0.py"
---

Perfecto, Bird. Te paso un ejemplo completo de **`fm.py`** tipo CLI usando `argparse`, que cumple con todo lo que pediste: crear, borrar, mover, listar archivos, con metadatos y un CSV de índice.

## Script

fm_v0.1.0.py

---

### Ejemplos de uso desde terminal

```bash
# Crear un script Python
python3 fm.py crear nuevo_script script .py --location src

# Crear un documento Markdown en doc/context
python3 fm.py crear documento doc .md --location doc

# Borrar archivo o carpeta
python3 fm.py borrar src/nuevo_script/nuevo_script.py

# Mover archivo
python3 fm.py mover doc/documento/documento.md doc/documento/nuevo_lugar/documento.md

# Listar archivos .py
python3 fm.py listar --ext .py
```

---

✅ Ventajas de este enfoque:

* No recrea toda la estructura global al crear un archivo.
* Carpeta contenedora automática para cada archivo.
* Metadatos iniciales en cada archivo.
* CSV de índice actualizado automáticamente.
* CLI sencillo con `argparse`.

---

Si querés, Bird, puedo hacer una **versión mejorada con alias de rutas y soporte de todos los tipos de extensión automáticamente**, para no tener que pasar siempre `--location` ni manejar `.py`, `.md`, `.yaml` manualmente.

¿Querés que haga esa versión optimizada?
