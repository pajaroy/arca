---
type: idea_base
title: "Arquitectura de prompts para scripts en Python"
author: "Bird"
date: 2025-08-23
tags: [prompt, python, modular, config, base]
version: 1.0
---

# 🧩 Estructura del Prompt
Este es el molde base. Cada sección marcada con [CORCHETES] debe reemplazarse al momento de pedir un prompt.


```yaml
Quiero que actúes como \[ROL].
Tu tarea es \[OBJETIVO].
Debes considerar:

* Entorno base: ROOT = \~/trece/.dev
* Siempre importar config: `from config.config import config`
* Usar arquitectura modular en Python.
* Cumplir los siguientes requisitos: \[REQUISITOS].

El output esperado es \[FORMATO].
```

---

# 🎯 Objetivo
Explicar la finalidad general de este prompt (ejemplo: generar scripts Python modulares usando la config central).

# 📋 Contexto
Indicar en qué escenario se aplicará (automatización, procesamiento de datos, asistentes, etc.).

# 🔑 Requisitos
Lista de condiciones que siempre se deben cumplir, además de las pautas fijas arriba.  
Ejemplo:  
- El script debe ser ejecutable desde CLI.  
- Comentarios claros en el código.  
- Usar pathlib en vez de os.path.

# 🖥️ Ejemplo de Uso
Ejemplo práctico aplicando la estructura:  

```yaml
Quiero que actúes como arquitecto de programación en Python.
Tu tarea es generar un script que lea todos los CSV en \~/trece/data/input y los combine en un único archivo `output.csv`.
Debes considerar:

* Entorno base: ROOT = \~/trece/.dev
* Siempre importar config: `from config.config import config`
* Usar arquitectura modular en Python.
* Cumplir los siguientes requisitos:

  * El script debe usar pandas.
  * Guardar el resultado en \~/trece/data/output.

El output esperado es un script en Python con funciones bien separadas.
```

# 📂 Relación con Scripts
- Ejemplo: `src/core/merge_csv.py`

# ✅ Criterios de Éxito
- El prompt genera siempre un script funcional y modular.  
- El asistente entiende el entorno ROOT y la config central.  
```

---

👉 Ventajas de este diseño:

* **Estructura limpia al inicio** → tu prompt ya nace con forma clara.
* **Pautas globales fijas** → no tenés que repetir lo del ROOT ni el import de config cada vez.
* **\[PLACEHOLDERS] definidos** → podés automatizar su reemplazo con un script (por ejemplo un mini parser que reemplace `[OBJETIVO]`, `[REQUISITOS]`, etc.).

---

¿Querés que te arme también un **script en Python** que lea un `idea_base.md`, detecte los placeholders y genere un `prompt.md` listo para usar reemplazando lo que le pases como inputs?
