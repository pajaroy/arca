# ---
# type: "script"
# fecha: "2025-08-19"
# version: "0.1.0"
# descripcion: "Calcula los stock por harvest"
# ---
import pandas as pd

# Cargo las tablas
harvest = pd.read_csv("data/harvest.csv")
harvest_detail = pd.read_csv("data/harvest_detail.csv")

# Agrupar harvest_detail y sumar los gramos
stock = harvest_detail.groupby("harvest_id")["grams"].sum().reset_index()

# Unir con harvest para tener la info completa
resultado = pd.merge(harvest, stock, left_on="id", right_on="harvest_id", how="left")

# Mostrar resultado
print(resultado[["id", "cut_date", "description", "grams"]])
