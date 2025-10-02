# 📁 Carpeta `data/`

Esta carpeta contiene **toda la estructura de datos** utilizada por el sistema principal (`main.py`). Se organiza en etapas de procesamiento progresivas, respetando buenas prácticas de trazabilidad, escalabilidad y reutilización en flujos de machine learning y análisis automatizado.

---

## 📐 Estructura general

```bash
/data/
├── raw/         # Datos crudos sin procesar, tal como fueron obtenidos
├── staging/     # Zona temporal para limpieza, validación y preprocesamiento
├── processed/   # Datos estructurados con metadatos extraídos y listos para análisis
├── features/    # Representaciones vectoriales, embeddings u otros features derivados
├── models/      # (Opcional) Modelos entrenados sobre los datos procesados
└── logs/        # Logs del procesamiento, errores, auditorías y trazabilidad
```

---

## 🧱 Descripción por carpeta

### `/raw/`
- Aquí se almacenan los archivos originales (Markdown, YAML, scripts, etc.).
- **No deben modificarse** ni sobrescribirse.
- Se acepta desorden, duplicación y formatos variados.
- Puede tener subcarpetas por tipo (`/raw/md/`, `/raw/yaml/`, etc.).

### `/staging/`
- Espacio de trabajo intermedio.
- Aquí se calcula el **hash** de los archivos, se detectan duplicados y se extraen estructuras básicas.
- Se valida el formato de los datos antes de pasarlos a la siguiente etapa.

### `/processed/`
- Archivos con metadatos extraídos, convertidos a formatos homogéneos (`.json`, `.csv`, etc.).
- Organizados e indexados por tema, autor, fecha o proyecto.
- Se considera la base consolidada para el análisis.

### `/features/`
- Representaciones numéricas útiles para aprendizaje automático (ej. vectores de texto, embeddings).
- Base para clustering, clasificación, búsqueda semántica, etc.

### `/models/` *(opcional)*
- Almacenamiento de modelos entrenados con estos datos.
- Se recomienda guardar metadata del modelo junto con el archivo (`.json`, `.pkl`, etc.).

### `/logs/`
- Registros del procesamiento: errores, acciones, timestamps, hash detectados.
- Útil para debugging y auditoría.

---

## 📌 Consideraciones

- Toda la configuración está centralizada en `config.yaml` en la raíz del proyecto.
- El punto de entrada del sistema es `main.py`, que debe respetar esta estructura.
- Se recomienda no eliminar ni modificar manualmente los archivos en `/staging/` o `/processed/`.

---

## ✅ Convenciones internas

- Los archivos procesados deben incluir:
  - Hash único del contenido (`blake3` recomendado).
  - Timestamp de procesamiento.
  - Fuente de origen (`raw_path`, etc.).
  - Etiquetas extraídas, si aplica.

- El sistema debe permitir re-procesar el `raw` sin duplicar datos ya presentes en `processed`.

---

## 📚 Próximos pasos sugeridos

- Agregar esquemas (`schemas/`) para validar tipos de datos en `staging`.
- Incorporar versionado semántico de datasets.
- Integrar un indexador semántico o motor de búsqueda (ej: con embeddings).
- Permitir retroalimentación al sistema para mejorar clasificación automatizada.

---

Este `README.md` debe mantenerse actualizado si se modifica la estructura de `data/`.
