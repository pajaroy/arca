# ---
# type: "script"
# fecha: "2025-08-19"
# version: "0.1.0"
# descripcion: "calcula los retiros por socio"
# ---
import pandas as pd
from pathlib import Path

# Rutas base
BASE_DIR = Path.home() / "trece"
DATA_DIR = BASE_DIR / "data/impositive"

# Cargar CSVs
entities = pd.read_csv(DATA_DIR / "entities.csv")
withdrawals = pd.read_csv(DATA_DIR / "withdrawals.csv")

# 🔹 Limpiar posibles columnas Unnamed
entities = entities.loc[:, ~entities.columns.str.contains("^Unnamed")]
withdrawals = withdrawals.loc[:, ~withdrawals.columns.str.contains("^Unnamed")]

# 🔹 Agrupar retiros por socio (entitie_id)
retiros = withdrawals.groupby("entitie_id")["grams"].sum().reset_index()

# 🔹 Unir con la tabla de socios para obtener nombres
retiros = pd.merge(retiros, entities, left_on="entitie_id", right_on="id", how="left")

# 🔹 Seleccionar columnas clave
retiros = retiros[["id", "name", "grams"]].rename(columns={"grams": "total_retirado"})

# 🔹 Mostrar en pantalla
print("📊 Total de retiros por socio:")
print(retiros.to_string(index=False))
