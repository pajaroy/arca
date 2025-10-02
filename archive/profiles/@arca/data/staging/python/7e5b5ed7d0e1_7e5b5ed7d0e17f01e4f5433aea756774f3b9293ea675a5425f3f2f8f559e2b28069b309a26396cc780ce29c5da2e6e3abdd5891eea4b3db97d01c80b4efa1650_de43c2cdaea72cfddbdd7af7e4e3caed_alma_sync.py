
""" 
ALMA SYNC - Núcleo de Operaciones del Sistema ALMA LIBRE
v0.8.0 | Versión modularizada
"""

import sys
from alma_core import write_memory, read_memories, validate_memorias, backup_memorias

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Uso: python alma_sync.py [write|read|validate|backup]")
        sys.exit(1)

    accion = sys.argv[1]

    if accion == "write":
        write_memory()
    elif accion == "read":
        read_memories()
    elif accion == "validate":
        validate_memorias()
    elif accion == "backup":
        backup_memorias()
    else:
        print(f"❌ Acción no reconocida: {accion}")
