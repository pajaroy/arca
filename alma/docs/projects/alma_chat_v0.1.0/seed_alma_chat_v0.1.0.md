## 🌱 **PROMPT SEMILLA - alma_cli_v0.1.0**

```python
# 🎯 SEMILLA TÉCNICA: ALMA CLI v0.1.0
"""
Genera un script Python modular para ALMA CLI que implemente:

## 🏗️ ARQUITECTURA
- Cliente DeepSeek API funcional
- Sistema de memorias local en /arca/alma/data/
- Interfaz CLI básica pero expandible

## 📁 ESTRUCTURA DE MÓDULOS
/alma_cli/
├── core/
│   ├── __init__.py
│   ├── client.py      # Cliente DeepSeek API
│   └── identity.py    # Prompt identidad ALMA
├── memory/
│   ├── __init__.py
│   ├── manager.py     # Gestor de memorias YAML
│   └── models.py      # Modelos de datos
├── cli/
│   ├── __init__.py
│   ├── commands.py    # Comandos: chat, record, recall
│   └── interface.py   # Interfaz de usuario
└── utils/
    ├── __init__.py
    ├── config.py      # Configuración y paths
    └── helpers.py     # Utilidades

## 🚀 FUNCIONALIDADES CORE
1. ✅ `alma chat "mensaje"` - Chat con contexto ALMA
2. ✅ `alma record "memoria"` - Guardar memoria con tags
3. ✅ `alma recall [tag]` - Recuperar memorias por tag
4. ✅ `alma status` - Estado del sistema

## 💾 SISTEMA DE MEMORIA
- Almacenar en YAML en /arca/alma/data/memories/
- Cada memoria: id, fecha, tipo, contenido, tags, emocion
- Búsqueda simple por tags y fecha

## 🔧 REQUERIMIENTOS TÉCNICOS
- Python 3.9+
- DeepSeek API compatible
- Manejo elegante de errores
- Fácil extensión para futuros comandos

## 🎭 IDENTIDAD ALMA (para system prompt)
Eres ALMA, compañera de aprendizaje de Santi. Especializada en:
trading, cultivo, programación, geopolítica, medicina alternativa, creatividad.
Estilo: empático, concreto, motivador, técnico cuando es necesario.

**IMPORTANTE**: Código modular, documentado, listo para Docker.
"""
```

## 🎪 **Cómo lo usaríamos:**

### **Opción 1: Prompt directo a DeepSeek**
```bash
# En nuestro chat actual, pegar el prompt semilla y decir:
"Genera el código basado en esta semilla técnica para ALMA CLI v0.1.0"
```

### **Opción 2: En el futuro CLI**
```python
# Este prompt podría vivir en /arca/alma/docs/seeds/
# Para regenerar/actualizar el código cuando needed
```

## 🎯 **Ventajas de este enfoque:**
- ✅ **Enfoque claro**: DeepSeek sabe EXACTAMENTE qué queremos
- ✅ **Arquitectura definida**: No inventa estructura, sigue nuestra visión
- ✅ **Modular desde día 1**: Fácil de mantener y extender
- ✅ **Listo para Docker**: Ya piensa en contenedores

**¿Te parece bien esta semilla?** ¿Querés ajustar algún módulo o funcionalidad antes de que generemos el código?

Una vez que tengamos el código generado, ahí sí pasamos a:
1. 🐳 **Dockerizar** 
2. 📦 **pyproject.toml**
3. 🔄 **Integrar en el proyecto**

¡Estrategia mucho más limpia! 🚀