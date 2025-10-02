---
date: "2025-09-27"
name: "contex_13cc"
type: "context"
version: "0.1.0"
description: "Contexto explicativo de trece cannabis club"
linked_to: [/trece]
---
# 📖 Contexto Institucional – 13 Cannabis Club (13CC)

Este documento organiza la información central de **trece** para mantener claridad en la misión, estructura y lineamientos del proyecto.

---

## 🎯 Visión

Construir una comunidad productiva, organizada y legalmente respaldada en torno al cultivo de cannabis, con objetivos sociales, terapéuticos y económicos.  
Escalar la operación con un enfoque profesional, modular y tecnológicamente avanzado.

---

## 🧱 Estructura Organizacional

- **Club Madre – 13CC**  
  Entidad central que coordina gestión institucional, legal y contable.  
  Responsabilidades: archivo de actas, estatutos, balances, relaciones institucionales.

- **Anexos Operativos**  
  Descentralizados, enfocados en producción, logística, distribución y apoyo social.

---

## 🗂️ Áreas del Proyecto

1. **Contabilidad**  
   - Gestión de balances, ingresos/egresos, pagos y presupuestos.  
   - Automatización con scripts Python (pandas, sqlite, scikit-learn para proyecciones).  

2. **Documentación Legal**  
   - Actas, estatutos, normativas vigentes.  
   - Archivo en `/docs/legal/`.

3. **Proyectos e Innovación**  
   - Iniciativas en desarrollo (`/docs/projects/`).  
   - Ejemplo: *impositive_to_dev* como plan de integración fiscal.

4. **Meta y Configuración**  
   - Configuraciones en `/config/` y `/meta/`.  

---

## 🔧 Tecnologías

- **Python 3.11**  
- Librerías principales: pandas, numpy, scikit-learn, ruamel.yaml, chromadb, typer, rich, loguru.  
- **SQLite** como base de datos local.  
- **Docker** para entornos reproducibles.  

---

## ✅ Buenas prácticas

- Mantener cada subproyecto **modular e independiente** dentro de Arca.  
- Uso de `pyproject.toml` para dependencias.  
- Scripts de backup y versionado antes de integrar con otros módulos.  
- Documentación clara y progresiva (`README.md` + docs específicos).
