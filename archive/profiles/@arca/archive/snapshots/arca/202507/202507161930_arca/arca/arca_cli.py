"""METADATOS\nuuid: fdb26829-7fba-43dd-8848-85cf6651fbff
tipo: py
nombre: arca_cli
version: 0.1.0
estado: activo
fecha_creacion: '2025-07-16T01:46:44.068646'
fecha_modificacion: '2025-07-16T01:46:44.068711'
autor: Bird
descripcion: Terminal cli gestor de archivos
hash_integridad: fd4e3e5cc33d5cb5188bcc49900e24db42d18725ce67bcf9bb1e4e72607fb567
\n"""

import sys
import importlib
from load_config import load_config

def show_header(comandos):
    print("=" * 45)
    print("             🌐  ARCA - Terminal CLI  🌐")
    print("=" * 45)
    print("Comandos disponibles: " + " | ".join(list(comandos.keys()) + ["salir"]))
    print()

def main():
    CONFIG = load_config()['config']
    comandos = CONFIG['comandos']
    show_header(comandos)
    while True:
        try:
            comando = input("ARCA > ").strip().lower()
            if comando in ("salir", "exit", "quit"):
                print("Cerrando ARCA CLI.")
                break
            elif comando in comandos:
                info = comandos[comando]
                modulo = importlib.import_module(info["modulo"])
                funcion = getattr(modulo, info["funcion"])
                args = []
                for param in info["parametros"]:
                    val = input(f"{param.capitalize()}: ").strip()
                    args.append(val)
                try:
                    kwargs = dict(zip(info["parametros"], args))
                    funcion(**kwargs)   # <--- CAMBIA ACÁ
                except Exception as e:
                    print(f"Error ejecutando '{comando}': {e}")

            elif comando == "":
                continue
            else:
                print("Comando no reconocido. Usa alguno de: " + ", ".join(comandos.keys()) + " o salir.")
        except KeyboardInterrupt:
            print("\nCerrando ARCA CLI.")
            break

if __name__ == "__main__":
    main()
