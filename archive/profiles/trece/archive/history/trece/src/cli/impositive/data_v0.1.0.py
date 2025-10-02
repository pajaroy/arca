# ---
# type: "script"
# fecha: "2025-08-20"
# version: "0.1.0"
# descripcion: "terminal contable de 13cc"
# ---
# data_cli.py
import pandas as pd
import cmd
import os
from datetime import datetime, timedelta
import calendar
import sys

class DataCLI(cmd.Cmd):
    intro = """
    =============================================
    TERMINAL PERSISTENTE PARA GESTIÓN DE PLANILLAS CSV
    =============================================
    Escribe 'help' para ver los comandos disponibles
    o 'help <comando>' para ayuda específica.
    """
    prompt = "data_cli> "
    
    def __init__(self):
        super().__init__()
        self.data_path = "data/"
        self.load_all_data()
    
    def load_all_data(self):
        """Carga todos los archivos CSV en DataFrames"""
        try:
            self.concepts = pd.read_csv(os.path.join(self.data_path, "concepts.csv"))
            self.entities = pd.read_csv(os.path.join(self.data_path, "entities.csv"))
            self.entities_types = pd.read_csv(os.path.join(self.data_path, "entities_types.csv"))
            self.expenses = pd.read_csv(os.path.join(self.data_path, "expenses.csv"))
            self.genetics = pd.read_csv(os.path.join(self.data_path, "genetics.csv"))
            self.harvest = pd.read_csv(os.path.join(self.data_path, "harvest.csv"))
            self.harvest_detail = pd.read_csv(os.path.join(self.data_path, "harvest_detail.csv"))
            self.modules = pd.read_csv(os.path.join(self.data_path, "modules.csv"))
            self.paymethods = pd.read_csv(os.path.join(self.data_path, "paymethods.csv"))
            self.prices = pd.read_csv(os.path.join(self.data_path, "prices.csv"))
            self.withdrawals = pd.read_csv(os.path.join(self.data_path, "withdrawals.csv"))
            
            # Convertir columnas de fecha si existen
            for df_name in ["expenses", "harvest", "withdrawals"]:
                df = getattr(self, df_name)
                if "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"])
            
            print("✓ Todos los datos cargados correctamente")
        except Exception as e:
            print(f"Error cargando datos: {e}")
            sys.exit(1)
    
    def do_balance_mes_actual(self, arg):
        """Calcula el balance del mes actual"""
        hoy = datetime.now()
        primer_dia_mes = hoy.replace(day=1)
        ultimo_dia_mes = hoy.replace(day=calendar.monthrange(hoy.year, hoy.month)[1])
        
        # Gastos del mes
        gastos_mes = self.expenses[
            (self.expenses["date"] >= primer_dia_mes) & 
            (self.expenses["date"] <= ultimo_dia_mes)
        ]["amount"].sum()
        
        # Retiros del mes
        retiros_mes = self.withdrawals[
            (self.withdrawals["date"] >= primer_dia_mes) & 
            (self.withdrawals["date"] <= ultimo_dia_mes)
        ]["amount"].sum()
        
        # Cálculo de ingresos (asumiendo que se calculan de alguna manera)
        # Esto es un placeholder - necesitarías implementar tu lógica específica
        ingresos_mes = 0  # Reemplazar con cálculo real
        
        balance = ingresos_mes - gastos_mes - retiros_mes
        
        print(f"=== BALANCE MES ACTUAL ({hoy.strftime('%B %Y')}) ===")
        print(f"Ingresos: ${ingresos_mes:,.2f}")
        print(f"Gastos: ${gastos_mes:,.2f}")
        print(f"Retiros: ${retiros_mes:,.2f}")
        print(f"Balance: ${balance:,.2f}")
    
    def do_dashboard_mensual(self, arg):
        """Muestra un dashboard con resumen mensual"""
        hoy = datetime.now()
        primer_dia_mes = hoy.replace(day=1)
        ultimo_dia_mes = hoy.replace(day=calendar.monthrange(hoy.year, hoy.month)[1])
        
        # Gastos por concepto
        gastos_concepto = self.expenses[
            self.expenses["date"].between(primer_dia_mes, ultimo_dia_mes)
        ].merge(self.concepts, left_on="concept_id", right_on="id") \
         .groupby("name")["amount"].sum().sort_values(ascending=False)
        
        # Retiros por socio
        retiros_socio = self.withdrawals[
            self.withdrawals["date"].between(primer_dia_mes, ultimo_dia_mes)
        ].merge(self.entities, left_on="entitie_id", right_on="id") \
         .groupby("name")["amount"].sum().sort_values(ascending=False)
        
        print("=== DASHBOARD MENSUAL ===")
        print("\nGASTOS POR CONCEPTO:")
        print(gastos_concepto.to_string())
        
        print("\nRETIROS POR SOCIO:")
        print(retiros_socio.to_string())
    
    def do_gastos_por_entidad_y_concepto(self, arg):
        """Muestra gastos agrupados por entidad y concepto"""
        # Obtener el período del argumento o usar mes actual por defecto
        if arg:
            try:
                año, mes = map(int, arg.split('-'))
                primer_dia = datetime(año, mes, 1)
                ultimo_dia = datetime(año, mes, calendar.monthrange(año, mes)[1])
            except:
                print("Formato incorrecto. Use: AAAA-MM")
                return
        else:
            hoy = datetime.now()
            primer_dia = hoy.replace(day=1)
            ultimo_dia = hoy.replace(day=calendar.monthrange(hoy.year, hoy.month)[1])
        
        gastos_filtrados = self.expenses[
            self.expenses["date"].between(primer_dia, ultimo_dia)
        ]
        
        # Unir con entities y concepts para obtener nombres
        gastos_con_info = gastos_filtrados.merge(
            self.entities, left_on="entitie_id", right_on="id"
        ).merge(
            self.concepts, left_on="concept_id", right_on="id"
        )
        
        resultado = gastos_con_info.groupby(["name_x", "name_y"])["amount"].sum().unstack().fillna(0)
        
        print(f"=== GASTOS POR ENTIDAD Y CONCEPTO ({primer_dia.strftime('%B %Y')}) ===")
        print(resultado.to_string())
    
    def do_harvest_stock(self, arg):
        """Calcula el stock actual de cosechas"""
        # Sumar todas las cosechas
        total_cosechado = self.harvest_detail.merge(
            self.harvest, left_on="harvest_id", right_on="id"
        ).merge(
            self.genetics, left_on="genetic_id", right_on="id"
        ).groupby("name")["grams"].sum()
        
        # Sumar todos los retiros (asumiendo que withdrawals tiene columna grams)
        if "grams" in self.withdrawals.columns:
            total_retirado = self.withdrawals.merge(
                self.genetics, left_on="genetic_id", right_on="id"
            ).groupby("name")["grams"].sum()
        else:
            # Si no hay columna grams, asumimos que amount es en gramos
            total_retirado = self.withdrawals.merge(
                self.genetics, left_on="genetic_id", right_on="id"
            ).groupby("name")["amount"].sum()
        
        # Calcular stock
        stock = total_cosechado - total_retirado.reindex(total_cosechado.index, fill_value=0)
        
        print("=== STOCK DE COSECHAS ===")
        for genetic, cantidad in stock.items():
            print(f"{genetic}: {cantidad:,.2f} gramos")
    
    def do_retiros_por_socio(self, arg):
        """Muestra retiros agrupados por socio"""
        # Obtener el período del argumento o usar mes actual por defecto
        if arg:
            try:
                año, mes = map(int, arg.split('-'))
                primer_dia = datetime(año, mes, 1)
                ultimo_dia = datetime(año, mes, calendar.monthrange(año, mes)[1])
            except:
                print("Formato incorrecto. Use: AAAA-MM")
                return
        else:
            hoy = datetime.now()
            primer_dia = hoy.replace(day=1)
            ultimo_dia = hoy.replace(day=calendar.monthrange(hoy.year, hoy.month)[1])
        
        retiros_filtrados = self.withdrawals[
            self.withdrawals["date"].between(primer_dia, ultimo_dia)
        ]
        
        retiros_por_socio = retiros_filtrados.merge(
            self.entities, left_on="entitie_id", right_on="id"
        ).groupby("name")["amount"].sum().sort_values(ascending=False)
        
        print(f"=== RETIROS POR SOCIO ({primer_dia.strftime('%B %Y')}) ===")
        print(retiros_por_socio.to_string())
    
    def do_stock_actual(self, arg):
        """Muestra el stock actual (alias de harvest_stock)"""
        self.do_harvest_stock(arg)
    
    def do_sum_expenses(self, arg):
        """Suma todos los gastos"""
        total_gastos = self.expenses["amount"].sum()
        print(f"TOTAL GASTOS: ${total_gastos:,.2f}")
    
    def do_sum_withdrawals(self, arg):
        """Suma todos los retiros"""
        total_retiros = self.withdrawals["amount"].sum()
        print(f"TOTAL RETIROS: ${total_retiros:,.2f}")
    
    def do_reload(self, arg):
        """Recarga todos los datos desde los archivos CSV"""
        self.load_all_data()
        print("Datos recargados correctamente")
    
    def do_exit(self, arg):
        """Sale del terminal"""
        print("¡Hasta pronto!")
        return True
    
    def do_quit(self, arg):
        """Sale del terminal (alias de exit)"""
        return self.do_exit(arg)
    
    # Aliases para comandos
    do_bal = do_balance_mes_actual
    do_dash = do_dashboard_mensual
    do_gastos = do_gastos_por_entidad_y_concepto
    do_stock = do_harvest_stock
    do_retiros = do_retiros_por_socio
    do_gastos_totales = do_sum_expenses
    do_retiros_totales = do_sum_withdrawals

if __name__ == "__main__":
    DataCLI().cmdloop()