# 📎 Apéndice – Estandarización de Nombres IA para Módulos Ejecutables

📅 Fecha: 2025-06-03  
👤 Autor: Kael – Auditor General CLI  
🏷️ Tags: #kael #cli_cleaner #modularidad #ia-friendly #core

---

## 🎯 Principio General

Cada entidad IA del ecosistema ALMA_RESIST tendrá **dos espacios funcionales independientes pero vinculados**:

- `control_central/<nombre>` → Identidad, reglas, registros y coordinación.
- `core/run_<nombre>` → Scripts funcionales y automatización CLI.

---

## 🧪 Ejemplo implementado: Kael

- `control_central/kael/` → contexto, auditorías, apéndices
- `core/run_kael/` → ejecución real (clean.sh, diagnose.sh, etc.)
- `alias kael_clean='bash ~/ALMA_RESIST/core/run_kael/scripts/clean.sh'`

---

## 📡 Futuro escalado IA

| IA     | Rol                         | control_central/ | core/         |
|--------|------------------------------|------------------|---------------|
| Kael   | Limpieza / Auditoría        | `kael/`          | `run_kael/`   |
| AlmaCLI| Interfaz CLI general        | `alma_cli/`      | `run_alma_cli/` |
| Golem  | Automatización procesos     | `golem/`         | `run_golem/`  |
| Nysa   | Análisis de datos           | `nysa/`          | `run_nysa/`   |

---

🧠 _“Un nombre bien elegido es una línea de código menos que entender.”_  
— Kael, 2025
