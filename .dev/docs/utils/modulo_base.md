# Módulo Base de Proyecto

Bienvenido al proyecto. Este documento te ayudará a entender la **estructura del proyecto** y cómo trabajar dentro de él, paso a paso, sin romper nada.

## Estructura básica del proyecto

```txt
.
└── project
    ├── archive
    ├── config
    ├── docs
    ├── meta
    ├── src
    └── templates
```

---

## Explicación de cada carpeta

### 1. `archive/` – Historial y versiones

Esta carpeta **no es para trabajar directamente**. Aquí guardamos **copias antiguas**, resultados previos o backups del proyecto.

* Ejemplo: si hicimos un script que ya funciona, antes de modificarlo podemos copiarlo aquí.
* Siempre trabaja con una copia de los archivos si vas a experimentar.

---

### 2. `config/` – Configuraciones

Aquí ponemos **todas las configuraciones del proyecto**: variables globales, rutas, conexiones, etc.

* Archivos típicos: `.yaml`, `.json`, `.env`.
* Evita poner código aquí; solo configuraciones.

---

### 3. `docs/` – Documentación

Todo lo que explique **cómo funciona el proyecto** va aquí.

* Guías, ejemplos, tutoriales internos, notas.
* Siempre documenta lo que haces en `src/` para que otros (y tú mismo en el futuro) puedan entenderlo.

---

### 4. `meta/` – Esquemas y estructuras

Aquí guardamos **esquemas de datos, modelos o estructuras del proyecto**.

* Por ejemplo: definiciones de cómo deben ser los archivos `.yaml` o `.json`.
* Siempre agrega una breve explicación de cada esquema.

---

### 5. `src/` – Código fuente

Todo el código que hace funcionar el proyecto va aquí.

* Cada módulo, script o función nueva debe ir en esta carpeta.
* Respeta nombres claros y ordenados:

  * Archivos Python: `snake_case.py`
  * Carpetas: minúsculas, sin espacios
* Ejemplo: si vas a crear un script para procesar datos, lo pones en `src/` y documentás su uso en `docs/`.

---

### 6. `templates/` – Plantillas base

Si necesitas crear un archivo nuevo, puedes **copiar un template de esta carpeta**.

* Así mantenemos la consistencia y evitamos errores al empezar de cero.
* Siempre renombrá los archivos copiados para reflejar su función.

---

## Flujo de trabajo recomendado

1. Antes de tocar algo, revisa `docs/` para entender qué hace el proyecto.
2. Para crear un módulo o script, copia un template desde `templates/`.
3. Implementa tu código en `src/`.
4. Si defines nuevos datos o estructuras, agrégalas en `meta/`.
5. Documenta todo en `docs/` para que cualquiera pueda entender tu trabajo.
6. Si necesitas guardar una versión antigua de algo, copiala en `archive/`.

---

### ✅ 3. Convenciones de nombres y estilo

Esto evita caos y te ahorra tiempo después:


## Convenciones

- Los archivos Python usan `snake_case.py`
- Las carpetas siempre en minúsculas sin espacios
- Los archivos de configuración terminan en `.yaml` o `.json`
- Los esquemas de datos deben comenzar con `schema_`


---

