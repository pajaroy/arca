"""
---
metadatos:
  id_unico: "scr-py-007"
  tipo: "prueba"
  nombre: "test_logger.py"
  version: "0.1.0"
  dependencias: ["logger.py"]
  descripcion: "Prueba unitaria del LoggerARCA"
---
"""
from logger import logger
from datetime import datetime
import pandas as pd
from pathlib import Path

def probar_logger():
    print("\n🔍 Iniciando prueba de LoggerARCA:")
    
    # 1. Generar logs de prueba
    logger.log("INFO", "test_logger", "Mensaje de prueba 1")
    logger.log("WARNING", "test_logger", "Mensaje de prueba 2")
    
    # 2. Forzar guardado (sin esperar 10 mensajes)
    if hasattr(logger, '_buffer'):
        print(f"\n⚠️ Buffer actual ({len(logger._buffer)} mensajes):")
        for msg in logger._buffer:
            print(f"- {msg['timestamp']} | {msg['nivel']}: {msg['mensaje']}")
        
        # Guardado manual
        logger._guardar()
        print("\n💾 Buffer guardado manualmente")
    else:
        print("❌ No se encontró buffer de logs")
    
    # 3. Verificar archivo generado
    archivo_log = next(Path(logger.ruta).glob("*.parquet"), None)
    if archivo_log:
        print(f"\n📄 Log generado en: {archivo_log}")
        df = pd.read_parquet(archivo_log)
        print("\nContenido del Parquet:")
        print(df.to_string(index=False))
    else:
        print("\n❌ No se encontraron archivos .parquet en:", logger.ruta)

if __name__ == "__main__":
    probar_logger()