---
uuid: 
tipo: requirements
formato: 
nombre: librerias
version: 0.1.0
estado: activo
fecha_creacion: 2025-07-16T18:44:00
fecha_modificacion: 2025-07-16T04:32:00.349261
autor: Bird
descripcion: Librerías Básicas para Proyecto Arca
hash_integridad:
---
#  Librerías Básicas para Proyecto Arca

## 🚀 Propósito

Este archivo documenta las **librerías principales** recomendadas para el desarrollo del sistema **Arca** (gestor documental + futura integración ML).

## Índice

Incluye librerías para:
- [[##  Librerías Recomendadas]]
- [[###  Gestión de archivos y rutas]]
- [[###  Cálculo de hashes]]
- [[### Lectura / Escritura de YAML]]
- [[### Indexación y bases de datos]]
- [[###  Machine Learning Básico]]
- [[### Logging]]
- [[###  CLI y Visualización]]
- [[##  Ejemplo de requirements.txt mínimo]]
- [[##  Recomendación]]
---

##  Librerías Recomendadas

###  **Gestión de archivos y rutas**

| Librería     | Descripción                                          |
|--------------|------------------------------------------------------|
| `pathlib`    | Manejo elegante y orientado a objetos de rutas.      |
| `shutil`     | Para mover/copiar/borrar trees enteros               |

---

###  **Cálculo de hashes**

| Librería     | Descripción                                          |
|--------------|------------------------------------------------------|
| `blake3`     | Hashing ultrarrápido y moderno (opcional).           |

---

###  **Lectura / Escritura de YAML**

| Librería         | Descripción                                      |
|------------------|--------------------------------------------------|
| `ruamel.yaml`    | Lectura y escritura avanzada de YAML.            |

---

### **Indexación y bases de datos**

| Librería         | Descripción                                      |
|------------------|--------------------------------------------------|
| `sqlite3`        | Base de datos embebida para índices.             |
| `chroma`         | Busqueda semantica - Vector store para RAG       |

---

###  **Machine Learning Básico**

| Librería         | Descripción                                      |
|------------------|--------------------------------------------------|
| `scikit-learn`   | Algoritmos clásicos de ML (clasificación, regresión, clustering). |
| `numpy`          | Cálculos numéricos.                              |
| `pandas`         | Manipulación de datasets tabulares.              |
| `joblib`         | Guardar modelos entrenados.                      |

---

###  **Logging**

| Librería         | Descripción                                      |
|------------------|--------------------------------------------------|
| `loguru`         | Logging avanzado y más elegante.                 |

---

###  **CLI y Visualización**

| Librería         | Descripción                                      |
|------------------|--------------------------------------------------|
| `typer`          | Alternativa moderna para CLI.                    |
| `rich`           | Imprimir textos coloridos y tablas en consola.    |
| `pytest`         | Para testear tus scripts.


---

##  Ejemplo de requirements.txt mínimo

```txt
blake3
shutil
ruamel.yaml
sqlite
chroma
scikit-learn
numpy
pandas
joblib
loguru
typer
rich
pytest
```

---

##  Recomendación

✅ **Usar librerías para low-level.**  
✅ **Desarrollar la lógica de Arca encima de estas.**  
✅ **Evitar reinventar la rueda.**  
✅ **Mantener un archivo como este para documentar dependencias.**

---

[[#  Librerías Básicas para Proyecto Arca]]

**Fin del documento.**