#!/usr/bin/env python3

from control_central.core.notebooks.cargar_memorias_v2 import gestor_memorias

# Ver estado actual
print("=== Estado inicial ===")
print("Memorias cargadas:", gestor_memorias.memorias)

# Añadir nueva memoria de prueba
nueva_memoria = {
    "prueba_1": {
        "tipo": "ejemplo",
        "contenido": "Esto es una prueba del sistema",
        "importancia": 5,
        "tags": ["test", "sistema"]
    }
}

gestor_memorias.actualizar(nueva_memoria)
print("\n=== Después de añadir prueba_1 ===")
print("Memorias:", gestor_memorias.memorias)
