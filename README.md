---
date: "2025-09-21"
name: "arca_readme"
type: "readme"
version: "0.1.0"
description: "Gestor documental modular de Alma"
linked_to: [/arca]
---
# Arca – Gestor de Archivos de Alma

**Arca** es el gestor documental modular dentro del ecosistema **ALMA_RESIST**.  
Su objetivo es **administrar archivos, metadatos, índices y logs** de forma segura, garantizando **integridad y trazabilidad**.  

Arca es la base para integrar:
- **Machine Learning** (entrenamiento sobre datasets propios).
- **Búsqueda semántica** de documentos.
- **Sistemas de versionado y archivado inteligente**.

---

## 📂 Estructura del proyecto

```txt
.
├── Dockerfile              # Imagen contenedor del proyecto Arca
├── README.md               # Descripción y estructura del proyecto
├── alma/                   # Modulo principal chat cli
├── archive/                # Archivador general, backups, versionado, temporales
├── config/                 # Configuraciones generales del proyecto
├── data/                   # Datasets y datos para aprendizaje
├── database/               # Base de datos en SQL del proyecto
├── docs/                   # Documentación del proyecto dividida en módulos
├── logs/                   # Logs centralizados y modulares
├── meta/                   # Schemas sql del proyecto
├── pyproject.toml          # Configuración base (poetry/docker)
├── src/                    # Código fuente del sistema
├── templates/              # Templates generales
├── test/                   # Campo de pruebas del proyecto
└── trece/                  # Proyecto ONG de cannabis
```

---

## Primeros pasos :

Ir a la carpeta raiz de Arca e iniciar el docker

### Comandos para iniciar docker

### Construir docker: 

docker build -t [proyecto] .

### Modo persistente : 

docker run -it -v $(pwd):/[app] --name [proyecto] [imagen] bash

---

## 🛠️ Funcionalidades actuales

* Gestión modular de archivos y metadatos.
* Registro de logs centralizados.
* Archivado y versionado básico.
* Integración con base de datos SQL.

---

## 🧭 Roadmap

* [ ] Integrar motor de búsqueda semántica.
* [ ] Indexación automática de metadatos.
* [ ] Conector con sistemas de IA para análisis de documentos.
* [ ] API REST para interacción externa.

---