# ---
# type: "script"
# fecha: "2025-08-19"
# version: "0.1.0"
# descripcion: "Suma expenses"
# ---

# import pandas as pd

# df = pd.read_csv("data/expenses.csv")
# print("Total amount:", df["amount"].sum())

import pandas as pd
from pathlib import Path

DATA_DIR = Path.home() / "trece/data/impositive"
df = pd.read_csv(DATA_DIR / "expenses.csv")

# Limpiar columnas Unnamed
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Asegurarse que la columna date sea datetime
df["date"] = pd.to_datetime(df["date"])

# Total general
print("📌 Total expenses (amount):", df["amount"].sum())

# Agrupar por mes
monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum()
print("\n📊 Expenses por mes:")
print(monthly)
