---
type: "prompt"
fecha: "2025-08-19"
version: "0.1.1"
descripcion: "Terminal contable 13cc"
---
**Solicitud de Terminal CLI Persistente para Gestión de Planillas CSV**

Necesito un terminal CLI interactivo y persistente que gestione cálculos sobre tablas CSV con la siguiente estructura y funcionalidades:

## 🎨 Diseño del Terminal:
- Muestra un "13" grande en ASCII art que permanezca visible siempre
- Interfaz colorida y organizada por secciones
- Prompt personalizado: `data_cli> `

## objetivo del terminal:

## 🔧 Funcionalidades Requeridas:
1. **balance_mes_actual** - Cálculo de balance del mes actual
2. **dashboard_mensual** - Resumen mensual con métricas clave
3. **gastos_por_entidad_y_concepto** - Agrupación de gastos
4. **harvest_stock** - Gestión de stock de cosechas
5. **retiros_por_socio** - Análisis de retiros por socio
6. **stock_actual** - Consulta de stock actualizado
7. **sum_expenses** - Sumatoria de gastos
8. **sum_withdrawals** - Sumatoria de retiros

## Estructura fisica :

```txt
[trece:~/trece]$ tree -l data
data
├── concepts.csv           # id,name,
├── entities.csv           # id,name,entities_type_id,tel,mail,notes,
├── entities_types.csv     # id,name,
├── expenses.csv           # id,date,amount,concept_id,entitie_id,caja_id,folio,description,notes
├── genetics.csv           # id,name,description,tag,
├── harvest.csv            # id,cut_date,module_id,description,notes,
├── harvest_detail.csv     # id,harvest_id,genetic_id,grams
├── modules.csv            # id,name,description
├── paymethods.csv         # id,name,
├── prices.csv             # id,name,amount
├── README.md            
└── withdrawals.csv        # id,date,entitie_id,genetic_id,harvest_id,grams,price_id,status,paymethod_id,notes,created_at
```

Sugerencias: en withdrawals deberia calcular grams por el precio qe marca el price_id para calcular el precio total para los balances

## 🎯 Comandos Adicionales:
- `reload` - Recargar datos sin salir del terminal
- `help` - Sistema de ayuda integrado
- `exit`/`quit` - Salir del terminal

## 📋 Especificaciones Técnicas:
- Desarrollado en Python con módulo `cmd`
- Manejo robusto de errores
- Carga eficiente de datos CSV
- Formateo de salida claro y legible
- Persistencia de sesión hasta comando exit

**Por favor proporciona el código completo del terminal CLI con estas especificaciones.**


## changelog:
version: 0.1.1

¡Claro que se puede agregar! No es necesario rehacer todo. Voy a agregar dos nuevos comandos para visualizar los retiros y gastos de forma paginada y con buen formato.

Aquí está el código actualizado con los nuevos comandos:

```python
import cmd
import csv
import os
import sys
from datetime import datetime, date
from collections import defaultdict

class TreceCLI(cmd.Cmd):
    intro = """
    \033[1;32m
      _______  _____  _____  ______ 
     |__   __|/ ____|/ ____||  ____|
        | |  | |    | |     | |__   
        | |  | |    | |     |  __|  
        | |  | |____| |____ | |____ 
        |_|   \_____|\_____||______|
    \033[0m
    Terminal de Gestión de Datos - Versión 1.0
    Escribe 'help' para ver los comandos disponibles.
    """
    prompt = '\033[1;34mdata_cli> \033[0m'
    
    def __init__(self):
        super().__init__()
        self.data_dir = "data"
        self.load_data()
        
    def load_data(self):
        """Carga todos los archivos CSV desde el directorio data"""
        self.data = {}
        try:
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.csv'):
                    name = filename[:-4]  # Remove .csv extension
                    filepath = os.path.join(self.data_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        self.data[name] = list(reader)
            print("\033[1;32m✓ Datos cargados correctamente\033[0m")
        except Exception as e:
            print(f"\033[1;31m✗ Error cargando datos: {e}\033[0m")
    
    def do_reload(self, arg):
        """Recargar datos sin salir del terminal"""
        self.load_data()
    
    def do_balance_mes_actual(self, arg):
        """Cálculo de balance del mes actual"""
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Calcular ingresos (retiros)
            ingresos = 0
            for retiro in self.data.get('withdrawals', []):
                fecha = datetime.strptime(retiro['date'], '%Y-%m-%d')
                if fecha.month == current_month and fecha.year == current_year:
                    # Buscar el precio correspondiente
                    precio_id = retiro['price_id']
                    precio = next((p for p in self.data.get('prices', []) 
                                  if p['id'] == precio_id), None)
                    if precio:
                        total_retiro = float(retiro['grams']) * float(precio['amount'])
                        ingresos += total_retiro
            
            # Calcular gastos
            gastos = 0
            for gasto in self.data.get('expenses', []):
                fecha = datetime.strptime(gasto['date'], '%Y-%m-%d')
                if fecha.month == current_month and fecha.year == current_year:
                    gastos += float(gasto['amount'])
            
            balance = ingresos - gastos
            
            print("\n" + "="*50)
            print("\033[1;36mBALANCE DEL MES ACTUAL\033[0m")
            print("="*50)
            print(f"Ingresos: \033[1;32m${ingresos:,.2f}\033[0m")
            print(f"Gastos: \033[1;31m${gastos:,.2f}\033[0m")
            print(f"Balance: \033[1;34m${balance:,.2f}\033[0m")
            print("="*50)
            
        except Exception as e:
            print(f"\033[1;31mError calculando balance: {e}\033[0m")
    
    def do_dashboard_mensual(self, arg):
        """Resumen mensual con métricas clave"""
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Inicializar métricas
            ingresos_totales = 0
            gastos_totales = 0
            retiros_por_socio = defaultdict(float)
            gastos_por_categoria = defaultdict(float)
            
            # Procesar retiros (ingresos)
            for retiro in self.data.get('withdrawals', []):
                fecha = datetime.strptime(retiro['date'], '%Y-%m-%d')
                if fecha.month == current_month and fecha.year == current_year:
                    precio_id = retiro['price_id']
                    precio = next((p for p in self.data.get('prices', []) 
                                  if p['id'] == precio_id), None)
                    if precio:
                        total_retiro = float(retiro['grams']) * float(precio['amount'])
                        ingresos_totales += total_retiro
                        
                        # Acumular por socio
                        socio_id = retiro['entitie_id']
                        socio = next((s for s in self.data.get('entities', []) 
                                     if s['id'] == socio_id), {'name': 'Desconocido'})
                        retiros_por_socio[socio['name']] += total_retiro
            
            # Procesar gastos
            for gasto in self.data.get('expenses', []):
                fecha = datetime.strptime(gasto['date'], '%Y-%m-%d')
                if fecha.month == current_month and fecha.year == current_year:
                    monto = float(gasto['amount'])
                    gastos_totales += monto
                    
                    # Acumular por concepto
                    concepto_id = gasto['concept_id']
                    concepto = next((c for c in self.data.get('concepts', []) 
                                    if c['id'] == concepto_id), {'name': 'Desconocido'})
                    gastos_por_categoria[concepto['name']] += monto
            
            balance = ingresos_totales - gastos_totales
            
            # Mostrar dashboard
            print("\n" + "="*60)
            print("\033[1;36mDASHBOARD MENSUAL\033[0m")
            print("="*60)
            print(f"Período: {current_month}/{current_year}")
            print(f"Ingresos Totales: \033[1;32m${ingresos_totales:,.2f}\033[0m")
            print(f"Gastos Totales: \033[1;31m${gastos_totales:,.2f}\033[0m")
            print(f"Balance Neto: \033[1;34m${balance:,.2f}\033[0m")
            print("-"*60)
            
            print("\n\033[1;33mRetiros por Socio:\033[0m")
            for socio, monto in sorted(retiros_por_socio.items(), key=lambda x: x[1], reverse=True):
                print(f"  {socio}: ${monto:,.2f}")
            
            print("\n\033[1;33mGastos por Categoría:\033[0m")
            for categoria, monto in sorted(gastos_por_categoria.items(), key=lambda x: x[1], reverse=True):
                print(f"  {categoria}: ${monto:,.2f}")
            
            print("="*60)
            
        except Exception as e:
            print(f"\033[1;31mError generando dashboard: {e}\033[0m")
    
    def do_gastos_por_entidad_y_concepto(self, arg):
        """Agrupación de gastos por entidad y concepto"""
        try:
            gastos_agrupados = defaultdict(lambda: defaultdict(float))
            
            for gasto in self.data.get('expenses', []):
                entidad_id = gasto['entitie_id']
                concepto_id = gasto['concept_id']
                monto = float(gasto['amount'])
                
                # Obtener nombres
                entidad = next((e for e in self.data.get('entities', []) 
                               if e['id'] == entidad_id), {'name': 'Desconocido'})
                concepto = next((c for c in self.data.get('concepts', []) 
                                if c['id'] == concepto_id), {'name': 'Desconocido'})
                
                gastos_agrupados[entidad['name']][concepto['name']] += monto
            
            # Mostrar resultados
            print("\n" + "="*70)
            print("\033[1;36mGASTOS POR ENTIDAD Y CONCEPTO\033[0m")
            print("="*70)
            
            for entidad, conceptos in gastos_agrupados.items():
                print(f"\n\033[1;33m{entidad}:\033[0m")
                total_entidad = sum(conceptos.values())
                for concepto, monto in sorted(conceptos.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {concepto}: ${monto:,.2f}")
                print(f"  \033[1;35mTotal: ${total_entidad:,.2f}\033[0m")
            
            print("="*70)
            
        except Exception as e:
            print(f"\033[1;31mError agrupando gastos: {e}\033[0m")
    
    def do_harvest_stock(self, arg):
        """Gestión de stock de cosechas"""
        try:
            # Calcular stock por genética
            stock_genetica = defaultdict(float)
            
            for detalle in self.data.get('harvest_detail', []):
                genetic_id = detalle['genetic_id']
                grams = float(detalle['grams'])
                
                # Restar retiros
                genetic_retiros = sum(
                    float(r['grams']) for r in self.data.get('withdrawals', [])
                    if r['genetic_id'] == genetic_id
                )
                
                net_grams = grams - genetic_retiros
                if net_grams > 0:
                    genetic_name = next(
                        (g['name'] for g in self.data.get('genetics', [])
                        if g['id'] == genetic_id), f"Genética {genetic_id}"
                    )
                    stock_genetica[genetic_name] += net_grams
            
            # Mostrar stock
            print("\n" + "="*50)
            print("\033[1;36mSTOCK DE COSECHAS\033[0m")
            print("="*50)
            
            if not stock_genetica:
                print("No hay stock disponible")
            else:
                for genetic, grams in sorted(stock_genetica.items()):
                    print(f"{genetic}: {grams:,.2f} gramos")
            
            print("="*50)
            
        except Exception as e:
            print(f"\033[1;31mError calculando stock: {e}\033[0m")
    
    def do_retiros_por_socio(self, arg):
        """Análisis de retiros por socio"""
        try:
            retiros_por_socio = defaultdict(float)
            
            for retiro in self.data.get('withdrawals', []):
                socio_id = retiro['entitie_id']
                precio_id = retiro['price_id']
                grams = float(retiro['grams'])
                
                # Obtener precio
                precio = next((p for p in self.data.get('prices', []) 
                              if p['id'] == precio_id), {'amount': '0'})
                monto = grams * float(precio['amount'])
                
                # Obtener nombre del socio
                socio = next((s for s in self.data.get('entities', []) 
                             if s['id'] == socio_id), {'name': f'Socio {socio_id}'})
                
                retiros_por_socio[socio['name']] += monto
            
            # Mostrar resultados
            print("\n" + "="*50)
            print("\033[1;36mRETIROS POR SOCIO\033[0m")
            print("="*50)
            
            total_retiros = sum(retiros_por_socio.values())
            for socio, monto in sorted(retiros_por_socio.items(), key=lambda x: x[1], reverse=True):
                porcentaje = (monto / total_retiros) * 100 if total_retiros > 0 else 0
                print(f"{socio}: ${monto:,.2f} ({porcentaje:.1f}%)")
            
            print("-"*50)
            print(f"\033[1;35mTOTAL: ${total_retiros:,.2f}\033[0m")
            print("="*50)
            
        except Exception as e:
            print(f"\033[1;31mError analizando retiros: {e}\033[0m")
    
    def do_stock_actual(self, arg):
        """Consulta de stock actualizado"""
        try:
            # Calcular stock total por genética
            stock = defaultdict(float)
            
            # Sumar todas las cosechas
            for detalle in self.data.get('harvest_detail', []):
                genetic_id = detalle['genetic_id']
                grams = float(detalle['grams'])
                stock[genetic_id] += grams
            
            # Restar todos los retiros
            for retiro in self.data.get('withdrawals', []):
                genetic_id = retiro['genetic_id']
                grams = float(retiro['grams'])
                stock[genetic_id] -= grams
            
            # Mostrar resultados
            print("\n" + "="*60)
            print("\033[1;36mSTOCK ACTUAL\033[0m")
            print("="*60)
            
            total_stock = 0
            for genetic_id, grams in stock.items():
                if grams > 0:
                    genetic_name = next(
                        (g['name'] for g in self.data.get('genetics', [])
                        if g['id'] == genetic_id), f"Genética {genetic_id}"
                    )
                    print(f"{genetic_name}: {grams:,.2f} gramos")
                    total_stock += grams
            
            print("-"*60)
            print(f"\033[1;35mSTOCK TOTAL: {total_stock:,.2f} gramos\033[0m")
            print("="*60)
            
        except Exception as e:
            print(f"\033[1;31mError consultando stock: {e}\033[0m")
    
    def do_sum_expenses(self, arg):
        """Sumatoria de gastos"""
        try:
            total = 0
            for gasto in self.data.get('expenses', []):
                total += float(gasto['amount'])
            
            print(f"\n\033[1;36mSUMATORIA DE GASTOS: \033[1;31m${total:,.2f}\033[0m\n")
            
        except Exception as e:
            print(f"\033[1;31mError sumando gastos: {e}\033[0m")
    
    def do_sum_withdrawals(self, arg):
        """Sumatoria de retiros"""
        try:
            total = 0
            for retiro in self.data.get('withdrawals', []):
                precio_id = retiro['price_id']
                grams = float(retiro['grams'])
                
                precio = next((p for p in self.data.get('prices', []) 
                              if p['id'] == precio_id), {'amount': '0'})
                total += grams * float(precio['amount'])
            
            print(f"\n\033[1;36mSUMATORIA DE RETIROS: \033[1;32m${total:,.2f}\033[0m\n")
            
        except Exception as e:
            print(f"\033[1;31mError sumando retiros: {e}\033[0m")
    
    def do_ver_retiros(self, arg):
        """Ver listado de retiros con paginación"""
        try:
            retiros = self.data.get('withdrawals', [])
            if not retiros:
                print("\033[1;33mNo hay retiros registrados\033[0m")
                return
            
            # Paginación
            page_size = 10
            page = 0
            total_pages = (len(retiros) + page_size - 1) // page_size
            
            while True:
                start_idx = page * page_size
                end_idx = min(start_idx + page_size, len(retiros))
                
                print(f"\n\033[1;36mRETIROS - Página {page + 1} de {total_pages}\033[0m")
                print("="*100)
                print(f"{'Fecha':<12} {'Socio':<20} {'Genética':<15} {'Gramos':<8} {'Precio':<10} {'Total':<12} {'Estado':<10}")
                print("-"*100)
                
                for i in range(start_idx, end_idx):
                    retiro = retiros[i]
                    
                    # Obtener información relacionada
                    socio = next((e for e in self.data.get('entities', []) 
                                 if e['id'] == retiro['entitie_id']), {'name': 'Desconocido'})
                    
                    genetic = next((g for g in self.data.get('genetics', []) 
                                   if g['id'] == retiro['genetic_id']), {'name': 'Desconocida'})
                    
                    precio_obj = next((p for p in self.data.get('prices', []) 
                                     if p['id'] == retiro['price_id']), {'amount': '0'})
                    
                    total = float(retiro['grams']) * float(precio_obj['amount'])
                    
                    print(f"{retiro['date']:<12} {socio['name'][:19]:<20} {genetic['name'][:14]:<15} "
                          f"{float(retiro['grams']):<8.2f} ${float(precio_obj['amount']):<9.2f} "
                          f"${total:<11.2f} {retiro['status'][:9]:<10}")
                
                print("-"*100)
                print(f"Mostrando {start_idx + 1}-{end_idx} de {len(retiros)} retiros")
                
                # Navegación
                if total_pages > 1:
                    print("\nNavegación: n(siguiente), p(anterior), número de página, q(salir)")
                    command = input("Opción: ").lower().strip()
                    
                    if command == 'q':
                        break
                    elif command == 'n' and page < total_pages - 1:
                        page += 1
                    elif command == 'p' and page > 0:
                        page -= 1
                    elif command.isdigit():
                        new_page = int(command) - 1
                        if 0 <= new_page < total_pages:
                            page = new_page
                        else:
                            print("\033[1;31mPágina no válida\033[0m")
                    else:
                        print("\033[1;31mOpción no válida\033[0m")
                else:
                    break
                    
        except Exception as e:
            print(f"\033[1;31mError mostrando retiros: {e}\033[0m")
    
    def do_ver_gastos(self, arg):
        """Ver listado de gastos con paginación"""
        try:
            gastos = self.data.get('expenses', [])
            if not gastos:
                print("\033[1;33mNo hay gastos registrados\033[0m")
                return
            
            # Paginación
            page_size = 10
            page = 0
            total_pages = (len(gastos) + page_size - 1) // page_size
            
            while True:
                start_idx = page * page_size
                end_idx = min(start_idx + page_size, len(gastos))
                
                print(f"\n\033[1;36mGASTOS - Página {page + 1} de {total_pages}\033[0m")
                print("="*90)
                print(f"{'Fecha':<12} {'Entidad':<20} {'Concepto':<20} {'Monto':<12} {'Descripción':<20}")
                print("-"*90)
                
                for i in range(start_idx, end_idx):
                    gasto = gastos[i]
                    
                    # Obtener información relacionada
                    entidad = next((e for e in self.data.get('entities', []) 
                                   if e['id'] == gasto['entitie_id']), {'name': 'Desconocido'})
                    
                    concepto = next((c for c in self.data.get('concepts', []) 
                                    if c['id'] == gasto['concept_id']), {'name': 'Desconocido'})
                    
                    descripcion = gasto.get('description', '')[:19]
                    
                    print(f"{gasto['date']:<12} {entidad['name'][:19]:<20} {concepto['name'][:19]:<20} "
                          f"${float(gasto['amount']):<11.2f} {descripcion:<20}")
                
                print("-"*90)
                print(f"Mostrando {start_idx + 1}-{end_idx} de {len(gastos)} gastos")
                
                # Navegación
                if total_pages > 1:
                    print("\nNavegación: n(siguiente), p(anterior), número de página, q(salir)")
                    command = input("Opción: ").lower().strip()
                    
                    if command == 'q':
                        break
                    elif command == 'n' and page < total_pages - 1:
                        page += 1
                    elif command == 'p' and page > 0:
                        page -= 1
                    elif command.isdigit():
                        new_page = int(command) - 1
                        if 0 <= new_page < total_pages:
                            page = new_page
                        else:
                            print("\033[1;31mPágina no válida\033[0m")
                    else:
                        print("\033[1;31mOpción no válida\033[0m")
                else:
                    break
                    
        except Exception as e:
            print(f"\033[1;31mError mostrando gastos: {e}\033[0m")
    
    def do_help(self, arg):
        """Sistema de ayuda integrado"""
        help_text = """
\033[1;36mCOMANDOS DISPONIBLES:\033[0m

  \033[1;33mbalance_mes_actual\033[0m      - Cálculo de balance del mes actual
  \033[1;33mdashboard_mensual\033[0m       - Resumen mensual con métricas clave
  \033[1;33mgastos_por_entidad_y_concepto\033[0m - Agrupación de gastos
  \033[1;33mharvest_stock\033[0m           - Gestión de stock de cosechas
  \033[1;33mretiros_por_socio\033[0m       - Análisis de retiros por socio
  \033[1;33mstock_actual\033[0m            - Consulta de stock actualizado
  \033[1;33msum_expenses\033[0m            - Sumatoria de gastos
  \033[1;33msum_withdrawals\033[0m         - Sumatoria de retiros
  \033[1;33mver_retiros\033[0m             - Ver listado de retiros
  \033[1;33mver_gastos\033[0m              - Ver listado de gastos
  \033[1;33mreload\033[0m                  - Recargar datos sin salir del terminal
  \033[1;33mhelp\033[0m                    - Mostrar esta ayuda
  \033[1;33mexit\033[0m                    - Salir del terminal
"""
        print(help_text)
    
    def do_exit(self, arg):
        """Salir del terminal"""
        print("\033[1;32m¡Hasta pronto!\033[0m")
        return True
    
    def do_quit(self, arg):
        """Salir del terminal"""
        return self.do_exit(arg)
    
    def emptyline(self):
        """No hacer nada cuando se presiona Enter sin comando"""
        pass

if __name__ == '__main__':
    # Verificar que existe el directorio data
    if not os.path.exists('data'):
        print("\033[1;31mError: No se encuentra el directorio 'data'\033[0m")
        print("Asegúrate de que el directorio existe y contiene los archivos CSV necesarios.")
        sys.exit(1)
    
    # Iniciar terminal
    cli = TreceCLI()
    cli.cmdloop()
```

## Nuevas funcionalidades agregadas:

1. **`ver_retiros`** - Muestra un listado paginado de todos los retiros con:
   - Fecha
   - Socio
   - Genética
   - Gramos
   - Precio unitario
   - Total
   - Estado

2. **`ver_gastos`** - Muestra un listado paginado de todos los gastos con:
   - Fecha
   - Entidad
   - Concepto
   - Monto
   - Descripción

## Características de los nuevos comandos:

- ✅ **Paginación inteligente**: Muestra 10 registros por página
- ✅ **Navegación**: Permite avanzar, retroceder y saltar a páginas específicas
- ✅ **Información relacionada**: Muestra nombres en lugar de IDs
- ✅ **Formato tabular**: Información organizada en columnas
- ✅ **Manejo de errores**: Robustez ante datos faltantes

Los comandos se integran perfectamente con el sistema existente sin necesidad de modificar la estructura base.





