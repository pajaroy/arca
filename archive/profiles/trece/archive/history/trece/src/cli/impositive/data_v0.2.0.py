# ---
# type: "script"
# fecha: "2025-08-20"
# version: "0.2.0"
# descripcion: "terminal contable de 13cc - versión mejorada"
# changelog: "Adaptación a nueva estructura de archivos, optimizaciones y nuevas funcionalidades"
# ---
import cmd
import csv
import os
import sys
from datetime import datetime, date
from collections import defaultdict

class TreceCLI(cmd.Cmd):
    intro = """
                13 Cannabis Club
    Terminal de Gestión de Datos - Versión 0.2.0
    Escribe 'help' para ver los comandos disponibles.
    """
    prompt = '\033[1;34mdata_cli> \033[0m'
    
    def __init__(self):
        super().__init__()
        self.data_dir = "data"
        self.data = {}
        self.indexes = {}  # Para optimizar búsquedas
        self.load_data()
        
    def build_indexes(self):
        """Construye índices para optimizar búsquedas"""
        self.indexes = {
            'entities': {item['id']: item for item in self.data.get('entities', [])},
            'concepts': {item['id']: item for item in self.data.get('concepts', [])},
            'prices': {item['id']: item for item in self.data.get('prices', [])},
            'genetics': {item['id']: item for item in self.data.get('genetics', [])},
            'harvest': {item['id']: item for item in self.data.get('harvest', [])},
            'paymethods': {item['id']: item for item in self.data.get('paymethods', [])},
            'entities_types': {item['id']: item for item in self.data.get('entities_types', [])},
            'boxes': {item['id']: item for item in self.data.get('boxes', [])}
        }
        
    def load_data(self):
        """Carga todos los archivos CSV desde el directorio data y subdirectorios"""
        self.data = {}
        try:
            for root, dirs, files in os.walk(self.data_dir):
                for filename in files:
                    if filename.endswith('.csv'):
                        name = filename[:-4]  # Remove .csv extension
                        filepath = os.path.join(root, filename)
                        
                        # Evitar sobrescribir archivos con el mismo nombre en diferentes directorios
                        if name in self.data:
                            # Si ya existe, combinamos los datos
                            with open(filepath, 'r', encoding='utf-8') as f:
                                reader = csv.DictReader(f)
                                self.data[name].extend(list(reader))
                        else:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                reader = csv.DictReader(f)
                                self.data[name] = list(reader)
            
            self.build_indexes()
            print("\033[1;32m✓ Datos cargados correctamente\033[0m")
            print(f"\033[1;36m✓ Se cargaron {len(self.data)} tablas de datos\033[0m")
            
        except Exception as e:
            print(f"\033[1;31m✗ Error cargando datos: {e}\033[0m")
    
    def get_entity_name(self, entity_id):
        """Obtiene el nombre de una entidad por su ID"""
        entity = self.indexes['entities'].get(entity_id, {'name': f'Entidad {entity_id}'})
        return entity['name']
    
    def get_concept_name(self, concept_id):
        """Obtiene el nombre de un concepto por su ID"""
        concept = self.indexes['concepts'].get(concept_id, {'name': f'Concepto {concept_id}'})
        return concept['name']
    
    def get_genetic_name(self, genetic_id):
        """Obtiene el nombre de una genética por su ID"""
        genetic = self.indexes['genetics'].get(genetic_id, {'name': f'Genética {genetic_id}'})
        return genetic['name']
    
    def get_price_amount(self, price_id):
        """Obtiene el monto de un precio por su ID"""
        price = self.indexes['prices'].get(price_id, {'amount': '0'})
        return float(price['amount'])
    
    def get_harvest_info(self, harvest_id):
        """Obtiene información de una cosecha por su ID"""
        harvest = self.indexes['harvest'].get(harvest_id, {
            'cut_date': 'Fecha desconocida', 
            'description': 'Sin descripción'
        })
        return harvest
    
    def do_reload(self, arg):
        """Recargar datos sin salir del terminal"""
        self.load_data()
    
    def do_balance_mes_actual(self, arg):
        """Cálculo de balance del mes actual considerando conceptos y estados"""
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Calcular ingresos (retiros confirmados)
            ingresos = 0
            ingresos_por_concepto = defaultdict(float)
            
            for retiro in self.data.get('withdrawals', []):
                try:
                    fecha = datetime.strptime(retiro['date'], '%Y-%m-%d')
                    if (fecha.month == current_month and fecha.year == current_year and 
                        retiro.get('status', 'completed') == 'completed'):
                        
                        total_retiro = float(retiro['grams']) * self.get_price_amount(retiro['price_id'])
                        ingresos += total_retiro
                        
                        # Agrupar por concepto
                        concepto_id = retiro.get('concept_id', '')
                        if concepto_id:
                            concepto_name = self.get_concept_name(concepto_id)
                            ingresos_por_concepto[concepto_name] += total_retiro
                except (ValueError, KeyError):
                    continue
            
            # Calcular gastos
            gastos = 0
            gastos_por_concepto = defaultdict(float)
            
            for gasto in self.data.get('expenses', []):
                try:
                    fecha = datetime.strptime(gasto['date'], '%Y-%m-%d')
                    if fecha.month == current_month and fecha.year == current_year:
                        monto = float(gasto['amount'])
                        gastos += monto
                        
                        # Agrupar por concepto
                        concepto_id = gasto.get('concept_id', '')
                        if concepto_id:
                            concepto_name = self.get_concept_name(concepto_id)
                            gastos_por_concepto[concepto_name] += monto
                except (ValueError, KeyError):
                    continue
            
            balance = ingresos - gastos
            
            # Mostrar resultados
            print("\n" + "="*60)
            print("\033[1;36mBALANCE DEL MES ACTUAL\033[0m")
            print("="*60)
            print(f"Período: {current_month}/{current_year}")
            print(f"Ingresos: \033[1;32m${ingresos:,.2f}\033[0m")
            print(f"Gastos: \033[1;31m${gastos:,.2f}\033[0m")
            print(f"Balance: \033[1;34m${balance:,.2f}\033[0m")
            
            # Desglose por conceptos
            if ingresos_por_concepto:
                print("\n\033[1;33mIngresos por Concepto:\033[0m")
                for concepto, monto in sorted(ingresos_por_concepto.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {concepto}: ${monto:,.2f}")
            
            if gastos_por_concepto:
                print("\n\033[1;33mGastos por Concepto:\033[0m")
                for concepto, monto in sorted(gastos_por_concepto.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {concepto}: ${monto:,.2f}")
            
            print("="*60)
            
        except Exception as e:
            print(f"\033[1;31mError calculando balance: {e}\033[0m")
    
    def do_dashboard_mensual(self, arg):
        """Resumen mensual con métricas clave mejorado"""
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Inicializar métricas
            ingresos_totales = 0
            gastos_totales = 0
            retiros_por_socio = defaultdict(float)
            gastos_por_categoria = defaultdict(float)
            retiros_por_concepto = defaultdict(float)
            
            # Procesar retiros (ingresos confirmados)
            for retiro in self.data.get('withdrawals', []):
                try:
                    fecha = datetime.strptime(retiro['date'], '%Y-%m-%d')
                    if (fecha.month == current_month and fecha.year == current_year and 
                        retiro.get('status', 'completed') == 'completed'):
                        
                        total_retiro = float(retiro['grams']) * self.get_price_amount(retiro['price_id'])
                        ingresos_totales += total_retiro
                        
                        # Acumular por socio
                        socio_id = retiro['entitie_id']
                        retiros_por_socio[self.get_entity_name(socio_id)] += total_retiro
                        
                        # Acumular por concepto
                        concepto_id = retiro.get('concept_id', '')
                        if concepto_id:
                            retiros_por_concepto[self.get_concept_name(concepto_id)] += total_retiro
                except (ValueError, KeyError):
                    continue
            
            # Procesar gastos
            for gasto in self.data.get('expenses', []):
                try:
                    fecha = datetime.strptime(gasto['date'], '%Y-%m-%d')
                    if fecha.month == current_month and fecha.year == current_year:
                        monto = float(gasto['amount'])
                        gastos_totales += monto
                        
                        # Acumular por concepto
                        concepto_id = gasto.get('concept_id', '')
                        if concepto_id:
                            gastos_por_categoria[self.get_concept_name(concepto_id)] += monto
                except (ValueError, KeyError):
                    continue
            
            balance = ingresos_totales - gastos_totales
            
            # Mostrar dashboard
            print("\n" + "="*70)
            print("\033[1;36mDASHBOARD MENSUAL\033[0m")
            print("="*70)
            print(f"Período: {current_month}/{current_year}")
            print(f"Ingresos Totales: \033[1;32m${ingresos_totales:,.2f}\033[0m")
            print(f"Gastos Totales: \033[1;31m${gastos_totales:,.2f}\033[0m")
            print(f"Balance Neto: \033[1;34m${balance:,.2f}\033[0m")
            print("-"*70)
            
            print("\n\033[1;33mRetiros por Socio:\033[0m")
            for socio, monto in sorted(retiros_por_socio.items(), key=lambda x: x[1], reverse=True)[:10]:  # Top 10
                porcentaje = (monto / ingresos_totales * 100) if ingresos_totales > 0 else 0
                print(f"  {socio[:25]:<25} ${monto:>8,.2f} ({porcentaje:5.1f}%)")
            
            print("\n\033[1;33mIngresos por Concepto:\033[0m")
            for concepto, monto in sorted(retiros_por_concepto.items(), key=lambda x: x[1], reverse=True):
                porcentaje = (monto / ingresos_totales * 100) if ingresos_totales > 0 else 0
                print(f"  {concepto[:25]:<25} ${monto:>8,.2f} ({porcentaje:5.1f}%)")
            
            print("\n\033[1;33mGastos por Categoría:\033[0m")
            for categoria, monto in sorted(gastos_por_categoria.items(), key=lambda x: x[1], reverse=True):
                porcentaje = (monto / gastos_totales * 100) if gastos_totales > 0 else 0
                print(f"  {categoria[:25]:<25} ${monto:>8,.2f} ({porcentaje:5.1f}%)")
            
            print("="*70)
            
        except Exception as e:
            print(f"\033[1;31mError generando dashboard: {e}\033[0m")
    
    def do_gastos_por_entidad_y_concepto(self, arg):
        """Agrupación de gastos por entidad y concepto con nuevos campos"""
        try:
            gastos_agrupados = defaultdict(lambda: defaultdict(float))
            
            for gasto in self.data.get('expenses', []):
                try:
                    entidad_id = gasto['entitie_id']
                    concepto_id = gasto.get('concept_id', '')
                    monto = float(gasto['amount'])
                    
                    # Obtener nombres
                    entidad_nombre = self.get_entity_name(entidad_id)
                    concepto_nombre = self.get_concept_name(concepto_id) if concepto_id else 'Sin concepto'
                    
                    gastos_agrupados[entidad_nombre][concepto_nombre] += monto
                except (ValueError, KeyError):
                    continue
            
            # Mostrar resultados
            print("\n" + "="*80)
            print("\033[1;36mGASTOS POR ENTIDAD Y CONCEPTO\033[0m")
            print("="*80)
            
            total_general = 0
            for entidad, conceptos in sorted(gastos_agrupados.items()):
                print(f"\n\033[1;33m{entidad}:\033[0m")
                total_entidad = sum(conceptos.values())
                total_general += total_entidad
                
                for concepto, monto in sorted(conceptos.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {concepto:<25} ${monto:>10,.2f}")
                
                print(f"  \033[1;35m{'TOTAL:':<25} ${total_entidad:>10,.2f}\033[0m")
            
            print("="*80)
            print(f"\033[1;36m{'TOTAL GENERAL:':<25} ${total_general:>10,.2f}\033[0m")
            print("="*80)
            
        except Exception as e:
            print(f"\033[1;31mError agrupando gastos: {e}\033[0m")
    
    def do_harvest_stock(self, arg):
        """Gestión de stock de cosechas con nueva estructura de datos"""
        try:
            # Diccionario para agrupar por cosecha y genética
            stock_por_cosecha = defaultdict(lambda: defaultdict(float))
            geneticas_en_cosecha = set()
            
            # Primero: sumar todos los detalles de cosecha
            for detalle in self.data.get('harvest_detail', []):
                try:
                    harvest_id = detalle['harvest_id']
                    genetic_id = detalle['genetic_id']
                    grams = float(detalle['grams'])
                    
                    genetic_name = self.get_genetic_name(genetic_id)
                    stock_por_cosecha[harvest_id][genetic_name] += grams
                    geneticas_en_cosecha.add(genetic_id)
                except (ValueError, KeyError):
                    continue
            
            # Segundo: restar retiros por cosecha y genética
            for retiro in self.data.get('withdrawals', []):
                try:
                    harvest_id = retiro.get('harvest_id', '')
                    genetic_id = retiro['genetic_id']
                    grams = float(retiro['grams'])
                    
                    if harvest_id and genetic_id in geneticas_en_cosecha:
                        genetic_name = self.get_genetic_name(genetic_id)
                        
                        if harvest_id in stock_por_cosecha and genetic_name in stock_por_cosecha[harvest_id]:
                            stock_por_cosecha[harvest_id][genetic_name] -= grams
                except (ValueError, KeyError):
                    continue
            
            # Mostrar resultados
            print("\n" + "="*80)
            print("\033[1;36mSTOCK DE COSECHAS POR COSECHA\033[0m")
            print("="*80)
            
            total_general = 0
            hay_stock = False
            
            for harvest_id, geneticas in sorted(stock_por_cosecha.items(), 
                                              key=lambda x: self.get_harvest_info(x[0])['cut_date'], 
                                              reverse=True):
                # Obtener info de la cosecha
                cosecha_info = self.get_harvest_info(harvest_id)
                
                print(f"\n\033[1;33mCosecha {harvest_id} - {cosecha_info['cut_date']}:\033[0m")
                print(f"Descripción: {cosecha_info['description']}")
                print("-" * 60)
                
                total_cosecha = 0
                for genetic_name, grams in sorted(geneticas.items()):
                    if grams > 0:
                        print(f"  {genetic_name:<20} {grams:>10,.2f} gramos")
                        total_cosecha += grams
                        total_general += grams
                        hay_stock = True
                
                if total_cosecha > 0:
                    print(f"  \033[1;35m{'TOTAL COSECHA:':<20} {total_cosecha:>10,.2f} gramos\033[0m")
            
            if not hay_stock:
                print("No hay stock disponible en cosechas")
            else:
                print(f"\n\033[1;32m{'STOCK GENERAL:':<20} {total_general:>10,.2f} gramos\033[0m")
            
            print("="*80)
            
        except Exception as e:
            print(f"\033[1;31mError calculando stock por cosecha: {e}\033[0m")
    
    def do_retiros_por_socio(self, arg):
        """Análisis de retiros por socio con nuevos campos"""
        try:
            retiros_por_socio = defaultdict(float)
            retiros_detalle = defaultdict(list)
            
            for retiro in self.data.get('withdrawals', []):
                try:
                    if retiro.get('status', 'completed') != 'completed':
                        continue
                    
                    socio_id = retiro['entitie_id']
                    grams = float(retiro['grams'])
                    monto = grams * self.get_price_amount(retiro['price_id'])
                    
                    socio_nombre = self.get_entity_name(socio_id)
                    retiros_por_socio[socio_nombre] += monto
                    
                    # Guardar detalle para mostrar después
                    retiros_detalle[socio_nombre].append({
                        'fecha': retiro['date'],
                        'genetic': self.get_genetic_name(retiro['genetic_id']),
                        'grams': grams,
                        'monto': monto,
                        'concepto': self.get_concept_name(retiro.get('concept_id', ''))
                    })
                except (ValueError, KeyError):
                    continue
            
            # Mostrar resultados
            print("\n" + "="*80)
            print("\033[1;36mRETIROS POR SOCIO\033[0m")
            print("="*80)
            
            total_retiros = sum(retiros_por_socio.values())
            
            for socio, monto_total in sorted(retiros_por_socio.items(), key=lambda x: x[1], reverse=True):
                porcentaje = (monto_total / total_retiros * 100) if total_retiros > 0 else 0
                print(f"\n\033[1;33m{socio}:\033[0m ${monto_total:,.2f} ({porcentaje:.1f}%)")
                
                # Mostrar detalles de los retiros de este socio
                for detalle in sorted(retiros_detalle[socio], key=lambda x: x['fecha']):
                    print(f"  {detalle['fecha']} {detalle['genetic'][:15]:<15} "
                          f"{detalle['grams']:>5.2f}g ${detalle['monto']:>8.2f} - {detalle['concepto']}")
            
            print("-"*80)
            print(f"\033[1;35mTOTAL: ${total_retiros:,.2f}\033[0m")
            print("="*80)
            
        except Exception as e:
            print(f"\033[1;31mError analizando retiros: {e}\033[0m")
    
    def do_stock_actual(self, arg):
        """Consulta de stock actualizado optimizada"""
        try:
            # Calcular stock total por genética
            stock = defaultdict(float)
            genetic_retiros = defaultdict(float)
            
            # Sumar todas las cosechas
            for detalle in self.data.get('harvest_detail', []):
                try:
                    genetic_id = detalle['genetic_id']
                    grams = float(detalle['grams'])
                    stock[genetic_id] += grams
                except (ValueError, KeyError):
                    continue
            
            # Restar todos los retiros
            for retiro in self.data.get('withdrawals', []):
                try:
                    genetic_id = retiro['genetic_id']
                    grams = float(retiro['grams'])
                    stock[genetic_id] -= grams
                    genetic_retiros[genetic_id] += grams
                except (ValueError, KeyError):
                    continue
            
            # Mostrar resultados
            print("\n" + "="*70)
            print("\033[1;36mSTOCK ACTUAL\033[0m")
            print("="*70)
            
            total_stock = 0
            total_retirado = 0
            
            # Crear lista para ordenamiento
            stock_list = []
            for genetic_id, grams in stock.items():
                genetic_name = self.get_genetic_name(genetic_id)
                retirado = genetic_retiros.get(genetic_id, 0)
                stock_list.append((genetic_name, grams, retirado))
                total_stock += grams
                total_retirado += retirado
            
            # Ordenar por stock descendente
            for genetic_name, grams, retirado in sorted(stock_list, key=lambda x: x[1], reverse=True):
                if grams > 0:
                    print(f"{genetic_name:<20} {grams:>10.2f} gramos (retirado: {retirado:>8.2f}g)")
            
            print("-"*70)
            print(f"\033[1;35mSTOCK TOTAL: {total_stock:>10.2f} gramos\033[0m")
            print(f"\033[1;35mRETIRADO TOTAL: {total_retirado:>8.2f} gramos\033[0m")
            print("="*70)
            
        except Exception as e:
            print(f"\033[1;31mError consultando stock: {e}\033[0m")
    
    def do_sum_expenses(self, arg):
        """Sumatoria de gastos con filtro por concepto"""
        try:
            total = 0
            gastos_por_concepto = defaultdict(float)
            
            for gasto in self.data.get('expenses', []):
                try:
                    monto = float(gasto['amount'])
                    total += monto
                    
                    concepto_id = gasto.get('concept_id', '')
                    concepto_nombre = self.get_concept_name(concepto_id) if concepto_id else 'Sin concepto'
                    gastos_por_concepto[concepto_nombre] += monto
                except (ValueError, KeyError):
                    continue
            
            print(f"\n\033[1;36mSUMATORIA DE GASTOS: \033[1;31m${total:,.2f}\033[0m")
            
            if gastos_por_concepto:
                print("\n\033[1;33mDesglose por concepto:\033[0m")
                for concepto, monto in sorted(gastos_por_concepto.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {concepto}: ${monto:,.2f}")
            
            print()
            
        except Exception as e:
            print(f"\033[1;31mError sumando gastos: {e}\033[0m")
    
    def do_sum_withdrawals(self, arg):
        """Sumatoria de retiros con filtro por estado y concepto"""
        try:
            total = 0
            retiros_por_concepto = defaultdict(float)
            retiros_por_estado = defaultdict(float)
            
            for retiro in self.data.get('withdrawals', []):
                try:
                    estado = retiro.get('status', 'completed')
                    if estado != 'completed' and arg != 'all':
                        continue
                    
                    grams = float(retiro['grams'])
                    monto = grams * self.get_price_amount(retiro['price_id'])
                    total += monto
                    
                    concepto_id = retiro.get('concept_id', '')
                    concepto_nombre = self.get_concept_name(concepto_id) if concepto_id else 'Sin concepto'
                    retiros_por_concepto[concepto_nombre] += monto
                    retiros_por_estado[estado] += monto
                except (ValueError, KeyError):
                    continue
            
            print(f"\n\033[1;36mSUMATORIA DE RETIROS: \033[1;32m${total:,.2f}\033[0m")
            
            if retiros_por_concepto:
                print("\n\033[1;33mDesglose por concepto:\033[0m")
                for concepto, monto in sorted(retiros_por_concepto.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {concepto}: ${monto:,.2f}")
            
            if retiros_por_estado:
                print("\n\033[1;33mDesglose por estado:\033[0m")
                for estado, monto in sorted(retiros_por_estado.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {estado}: ${monto:,.2f}")
            
            print()
            
        except Exception as e:
            print(f"\033[1;31mError sumando retiros: {e}\033[0m")
    
    def do_ver_retiros(self, arg):
        """Ver listado de retiros con paginación y nuevos campos"""
        try:
            retiros = self.data.get('withdrawals', [])
            if not retiros:
                print("\033[1;33mNo hay retiros registrados\033[0m")
                return
            
            # Filtrar por estado si se especifica
            filtro_estado = arg.lower() if arg else None
            if filtro_estado and filtro_estado != 'all':
                retiros = [r for r in retiros if r.get('status', '').lower() == filtro_estado]
            
            # Paginación
            page_size = 10
            page = 0
            total_pages = (len(retiros) + page_size - 1) // page_size
            
            while True:
                start_idx = page * page_size
                end_idx = min(start_idx + page_size, len(retiros))
                
                print(f"\n\033[1;36mRETIROS - Página {page + 1} de {total_pages}\033[0m")
                if filtro_estado:
                    print(f"Filtro: estado = {filtro_estado}")
                print("="*120)
                print(f"{'Fecha':<10} {'Socio':<20} {'Genética':<15} {'Grams':<6} {'Precio':<8} {'Total':<10} {'Estado':<10} {'Concepto':<15}")
                print("-"*120)
                
                for i in range(start_idx, end_idx):
                    retiro = retiros[i]
                    
                    # Obtener información relacionada
                    socio_nombre = self.get_entity_name(retiro['entitie_id'])
                    genetic_nombre = self.get_genetic_name(retiro['genetic_id'])
                    precio_monto = self.get_price_amount(retiro['price_id'])
                    total = float(retiro['grams']) * precio_monto
                    concepto_nombre = self.get_concept_name(retiro.get('concept_id', ''))
                    estado = retiro.get('status', 'unknown')
                    
                    print(f"{retiro['date']:<10} {socio_nombre[:19]:<20} {genetic_nombre[:14]:<15} "
                          f"{float(retiro['grams']):<6.2f} ${precio_monto:<7.2f} "
                          f"${total:<9.2f} {estado[:9]:<10} {concepto_nombre[:14]:<15}")
                
                print("-"*120)
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
        """Ver listado de gastos con paginación y nuevos campos"""
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
                print("="*100)
                print(f"{'Fecha':<10} {'Entidad':<20} {'Concepto':<20} {'Monto':<10} {'Caja':<10} {'Descripción':<20}")
                print("-"*100)
                
                for i in range(start_idx, end_idx):
                    gasto = gastos[i]
                    
                    # Obtener información relacionada
                    entidad_nombre = self.get_entity_name(gasto['entitie_id'])
                    concepto_nombre = self.get_concept_name(gasto.get('concept_id', ''))
                    caja_id = gasto.get('caja_id', '')
                    caja_nombre = self.indexes['boxes'].get(caja_id, {'name': 'Sin caja'})['name'] if caja_id else 'Sin caja'
                    descripcion = gasto.get('description', '')[:19]
                    
                    print(f"{gasto['date']:<10} {entidad_nombre[:19]:<20} {concepto_nombre[:19]:<20} "
                          f"${float(gasto['amount']):<9.2f} {caja_nombre[:9]:<10} {descripcion:<20}")
                
                print("-"*100)
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
    
    def do_estado_cajas(self, arg):
        """Muestra el estado actual de las cajas"""
        try:
            print("\n" + "="*80)
            print("\033[1;36mESTADO DE CAJAS\033[0m")
            print("="*80)
            
            # Calcular movimientos por caja
            movimientos_cajas = defaultdict(float)
            
            # Sumar gastos por caja
            for gasto in self.data.get('expenses', []):
                try:
                    caja_id = gasto.get('caja_id', '')
                    if caja_id:
                        monto = float(gasto['amount'])
                        movimientos_cajas[caja_id] -= monto
                except (ValueError, KeyError):
                    continue
            
            # Mostrar resultados
            for caja_id, balance in movimientos_cajas.items():
                caja = self.indexes['boxes'].get(caja_id, {'name': f'Caja {caja_id}', 'inicial': '0'})
                balance_total = float(caja.get('inicial', 0)) + balance
                
                print(f"{caja['name']:<20} Saldo inicial: ${float(caja.get('inicial', 0)):>10.2f} "
                      f"Movimientos: ${balance:>10.2f} Balance: ${balance_total:>10.2f}")
            
            print("="*80)
            
        except Exception as e:
            print(f"\033[1;31mError mostrando estado de cajas: {e}\033[0m")
    
    def do_help(self, arg):
        """Sistema de ayuda integrado"""
        help_text = """
\033[1;36mCOMANDOS DISPONIBLES:\033[0m

  \033[1;33mbalance_mes_actual\033[0m               - Cálculo de balance del mes actual
  \033[1;33mdashboard_mensual\033[0m                - Resumen mensual con métricas clave
  \033[1;33mgastos_por_entidad_y_concepto\033[0m    - Agrupación de gastos
  \033[1;33mharvest_stock\033[0m                    - Gestión de stock de cosechas
  \033[1;33mretiros_por_socio\033[0m                - Análisis de retiros por socio
  \033[1;33mstock_actual\033[0m                     - Consulta de stock actualizado
  \033[1;33msum_expenses\033[0m                     - Sumatoria de gastos
  \033[1;33msum_withdrawals\033[0m [all]            - Sumatoria de retiros (opcional: all=incluir todos los estados)
  \033[1;33mver_retiros\033[0m [estado]             - Ver listado de retiros (opcional: filtrar por estado)
  \033[1;33mver_gastos\033[0m                       - Ver listado de gastos
  \033[1;33mestado_cajas\033[0m                     - Estado actual de las cajas
  \033[1;33mreload\033[0m                           - Recargar datos sin salir del terminal
  \033[1;33mhelp\033[0m                             - Mostrar esta ayuda
  \033[1;33mexit\033[0m                             - Salir del terminal

\033[1;36mESTADOS DE RETIROS:\033[0m
  completed, pending, cancelled
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