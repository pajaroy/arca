import pandas as pd
from collections import Counter

def contar_palabras_csv(ruta_csv):
    # Leer CSV completo
    df = pd.read_csv(ruta_csv)
    
    # Aplanar toda la tabla a una sola lista de palabras
    palabras = df.astype(str).values.flatten()
    
    # Contar ocurrencias
    contador = Counter(palabras)
    
    # Mostrar resultados ordenados por frecuencia
    for palabra, freq in contador.most_common():
        print(f"{palabra}: {freq}")

if __name__ == "__main__":
    ruta = "~/trece/data/vege/05.csv"  # Cambiá por tu archivo
    contar_palabras_csv(ruta)
