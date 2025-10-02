# ---
# type: "script"
# fecha: "2025-08-19"
# version: "0.1.0"
# descripcion: "Calcula el stock actual"
# ---

import pandas as pd
from pathlib import Path

# Rutas base
BASE_DIR = Path.home() / "trece"
DATA_DIR = BASE_DIR / "data/impositive"

# Cargar CSVs
harvest_detail = pd.read_csv(DATA_DIR / "harvest_detail.csv")
withdrawals = pd.read_csv(DATA_DIR / "withdrawals.csv")
genetics = pd.read_csv(DATA_DIR / "genetics.csv")
harvest = pd.read_csv(DATA_DIR / "harvest.csv")

# 🔹 Limpiar posibles columnas Unnamed
harvest_detail = harvest_detail.loc[:, ~harvest_detail.columns.str.contains("^Unnamed")]
withdrawals = withdrawals.loc[:, ~withdrawals.columns.str.contains("^Unnamed")]
genetics = genetics.loc[:, ~genetics.columns.str.contains("^Unnamed")]
harvest = harvest.loc[:, ~harvest.columns.str.contains("^Unnamed")]

# 🔹 Agrupar withdrawals por harvest_id y genetic_id
retiros = withdrawals.groupby(["harvest_id", "genetic_id"])["grams"].sum().reset_index()
retiros = retiros.rename(columns={"grams": "total_retirado"})

# 🔹 Unir con harvest_detail para calcular stock actual
stock = pd.merge(harvest_detail, retiros, on=["harvest_id", "genetic_id"], how="left")
stock["total_retirado"] = stock["total_retirado"].fillna(0)
stock["stock_actual"] = stock["grams"] - stock["total_retirado"]

# 🔹 Agregar nombres de genetica y harvest para legibilidad
stock = pd.merge(stock, genetics, left_on="genetic_id", right_on="id", how="left", suffixes=("", "_genetic"))
stock = pd.merge(stock, harvest, left_on="harvest_id", right_on="id", how="left", suffixes=("", "_harvest"))

# 🔹 Seleccionar columnas clave
stock = stock[["harvest_id", "cut_date", "description", "genetic_id", "name", "stock_actual"]].rename(
    columns={"name": "genetic_name", "description": "harvest_description"}
)

# 🔹 Mostrar en pantalla
print("📊 Stock actual por harvest y genética:")
print(stock.to_string(index=False))
