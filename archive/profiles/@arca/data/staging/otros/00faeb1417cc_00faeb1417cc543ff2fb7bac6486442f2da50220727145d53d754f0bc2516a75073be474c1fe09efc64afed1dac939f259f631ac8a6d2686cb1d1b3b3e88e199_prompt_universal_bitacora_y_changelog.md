## PROMPT UNIVERSAL: Generar entrada triple de Bitácora y Changelog (MD/YAML/JSON)

**Instrucciones:**
Como IA asistente, generá una entrada de bitácora viva y de changelog vivo para el siguiente evento en un sistema documental crítico.  
Necesito que la salida esté en los tres formatos (Markdown, YAML y JSON), bien formateados y listos para pegar en archivos diferentes.  
Asegurate de:  
- Respetar los campos obligatorios: id, tipo, modulo, autor, fecha, status, tags, entradas (con fecha, accion, descripcion, motivo, ejecutado_por, estado/impacto).
- El id debe ser único y reflejar la fecha y tipo.
- La entrada debe estar en un array, incluso si es una sola.
- Todo debe ser válido para parsing automático (YAML/JSON sin errores de formato).

**Evento a registrar:**  
[Mencionar aquí la acción concreta, ejemplo: “Se movió prompt_base.md a archivo/downloads/historico/, autor: Santi, motivo: limpieza y archivo histórico.”]

---

**Tu output debe ser:**
1. Bitácora viva en Markdown
2. Bitácora viva en YAML
3. Bitácora viva en JSON
4. Changelog vivo en Markdown
5. Changelog vivo en YAML
6. Changelog vivo en JSON

Usá ejemplos realistas y no inventes más campos de los pedidos.

---
