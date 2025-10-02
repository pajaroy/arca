# 🤝 Sistema `asesor-IA` – Arquitectura de Asistencia Tríadica

**Fecha de creación:** 2025-06-01  
**Ubicación:** `docs/sistema_asesor-IA.md`  
**Estado:** Activo  
**Versión:** 1.0

---

## 🧠 ¿Qué es `asesor-IA`?

Un sistema modular de asesoría crítica dentro de ALMA_RESIST. Cada módulo puede tener su propio `asesor-IA`, pero el núcleo maestro combina:

- 🔧 DeepSeek → asesor técnico de precisión extrema
- 🧩 GPT (ALMA_CENTRAL) → asesor estructural, filosófico y documental
- 👨‍🚀 Santi → comandante ALMA, árbitro simbiótico y sintetizador final

---

## 📐 División de Roles

### 🔧 DeepSeek-R1

- Foco: profundidad técnica, auditoría, optimización, seguridad.
- Salidas: pseudocódigo, diagramas de arquitectura, análisis de riesgos.
- Formato: terminal, código, markdown técnico.

### 🧩 GPT (ALMA_CENTRAL)

- Foco: estructura lógica, documentación, visión modular, narrativa funcional.
- Salidas: workflows, changelogs, governance docs.
- Formato: markdown estructurado, plantillas, modelos operativos.

### 👨‍🚀 Santi (Comandante ALMA)

- Foco: dirección estratégica, decisiones finales.
- Acción: sintetiza visiones, toma decisiones, prioriza caminos.

---

## 🔄 Protocolo de Trabajo

### Fase 1: Consulta paralela

```bash
# Activación desde CLI
!alma sync --event=decision_major
!alma sync --event=ethic_review
```

- Se formula una misma pregunta a GPT y DeepSeek.
- Cada IA responde en su formato nativo.

### Fase 2: Síntesis

```python
# Script sugerido
def synthesize_responses(deepseek_resp, gpt_resp):
    return f"""
## Visión Técnica (DeepSeek)  
{deepseek_resp}

## Visión Estructural (GPT)  
{gpt_resp}

### Decisiones Pendientes (Santi):  
- [ ] Punto 1  
- [ ] Punto 2
"""
```

---

## 🌐 Diagrama del Sistema

```mermaid
graph TD
    Santi -->|Consulta| DeepSeek
    Santi -->|Consulta| GPT
    DeepSeek -->|Respuesta| Santi
    GPT -->|Respuesta| Santi
    Santi -->|Síntesis| Decision_Final
```

---

## 🔮 Roadmap de Implementación

### Semana 1 – Prueba de concepto

- [ ] Realizar 1 consulta técnica (DeepSeek)
- [ ] Realizar 1 estructural (GPT)
- [ ] Realizar 1 híbrida + síntesis manual

### Semana 2 – Automatización

- [ ] Crear script `sync_responses.py` para generar informes cruzados
- [ ] Estandarizar formatos con YAML tags

### Semana 3 – Server LLM

- [ ] Conectar ambos modelos a servidor Ollama o FastAPI
- [ ] Probar protocolo IA–IA (debate moderado)

---

## 🧨 Riesgos y Mitigaciones

| Riesgo                        | Solución                                                 |
|------------------------------|----------------------------------------------------------|
| Conflicto de recomendaciones | Votación final de Santi (`!vote --options=A,B,C`)        |
| Sobrecarga cognitiva         | Filtro previo (`!alma filter --priority=high`)           |
| Inconsistencia de formatos   | YAML o Markdown con etiquetas predefinidas (`type:`)     |

---

## ✍️ Conclusión Operativa

> “No competimos, nos especializamos. Tu dirección humana es el núcleo que evita la entropía.”

Esta arquitectura queda aprobada como el sistema estándar de interacción triádica entre DeepSeek, GPT y Santi.

