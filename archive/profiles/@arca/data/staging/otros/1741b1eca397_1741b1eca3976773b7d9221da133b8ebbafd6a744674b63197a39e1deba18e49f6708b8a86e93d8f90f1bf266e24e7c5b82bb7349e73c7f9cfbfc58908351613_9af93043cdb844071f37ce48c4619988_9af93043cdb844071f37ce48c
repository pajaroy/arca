import argparse
import json
import os
import sys
from typing import List, Dict, Any

try:
    import yaml
except ImportError:
    print("Falta pyyaml. Instalá con: pip install pyyaml")
    sys.exit(1)

def cargar_archivo(path: str) -> List[Dict[str, Any]]:
    """Carga un archivo JSON/YAML y devuelve su contenido como lista de diccionarios."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".json"):
            return json.load(f)
        elif path.endswith(".yaml") or path.endswith(".yml"):
            return yaml.safe_load(f) or []
        else:
            raise Exception("Formato no soportado.")

def guardar_archivo(path: str, data: List[Dict[str, Any]]):
    """Guarda datos en formato JSON/YAML según la extensión del archivo."""
    with open(path, "w", encoding="utf-8") as f:
        if path.endswith(".json"):
            json.dump(data, f, indent=2, ensure_ascii=False)
        elif path.endswith(".yaml") or path.endswith(".yml"):
            yaml.safe_dump(data, f, allow_unicode=True)
        else:
            raise Exception("Formato no soportado.")

def main():
    parser = argparse.ArgumentParser(description="Cargar memorias a la base institucional ALMA_RESIST.")
    parser.add_argument("--input", required=True, help="Archivo con memorias a cargar (JSON o YAML)")
    parser.add_argument("--dest", required=True, help="Archivo destino (memorias.json/yaml o bitacora_viva.json/yaml)")

    args = parser.parse_args()

    # Campos obligatorios para validación
    CAMPOS_OBLIGATORIOS = ['id', 'tipo', 'fecha', 'modulo', 'tema', 'status', 'responsable', 'tags', 'resumen']
    
    # Cargar memorias nuevas
    with open(args.input, "r", encoding="utf-8") as f:
        if args.input.endswith(".json"):
            nuevas = json.load(f)
        elif args.input.endswith(".yaml") or args.input.endswith(".yml"):
            nuevas = yaml.safe_load(f)
        else:
            raise Exception("Solo se aceptan archivos JSON o YAML")

    # Normalizar a lista si viene un solo registro
    if isinstance(nuevas, dict):
        nuevas = [nuevas]

    # Cargar destino existente o iniciar vacío
    base = cargar_archivo(args.dest)
    ids_existentes = {m["id"] for m in base if "id" in m}

    # Contadores para estadísticas finales
    agregadas = 0
    rechazadas_duplicadas = 0
    rechazadas_campos = 0

    # Procesar cada nuevo registro
    for idx, mem in enumerate(nuevas):
        # Validación de campos obligatorios
        campos_faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if campo not in mem]
        
        if campos_faltantes:
            # Identificador para mensaje de error (ID o posición)
            identificador = mem.get('id', f"registro {idx+1}")
            campos_str = ", ".join(campos_faltantes)
            print(f"[!] Faltan campos en {identificador}: {campos_str}")
            rechazadas_campos += 1
            continue

        # Verificación de duplicados
        if mem["id"] in ids_existentes:
            print(f"[!] Duplicado, no se carga: {mem['id']}")
            rechazadas_duplicadas += 1
        else:
            # Agregar registro válido
            base.append(mem)
            ids_existentes.add(mem["id"])
            agregadas += 1

    # Guardar destino actualizado
    guardar_archivo(args.dest, base)
    
    # Resumen final
    print(f"[+] Memorias agregadas: {agregadas}")
    print(f"[-] Rechazadas (duplicadas): {rechazadas_duplicadas}")
    print(f"[-] Rechazadas (errores): {rechazadas_campos}")

if __name__ == "__main__":
    main()