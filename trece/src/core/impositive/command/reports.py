import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from .db import db_manager

logger = logging.getLogger(__name__)

def generate_balance_report(month: str, detailed: bool = False):
    """Generar reporte de balance mensual"""
    try:
        # Validar formato de mes (YYYY-MM)
        year, month_num = map(int, month.split('-'))
        
        # Obtener ingresos por retiros
        income_result = db_manager.fetchone(
            """SELECT COALESCE(SUM(total_amount), 0) as total_income
               FROM withdrawals 
               WHERE strftime('%Y-%m', withdrawal_date) = ? AND status = 'completed'""",
            (month,)
        )
        total_income = income_result['total_income'] if income_result else 0.0
        
        # Obtener gastos
        expenses_result = db_manager.fetchone(
            """SELECT COALESCE(SUM(amount), 0) as total_expenses
               FROM expenses 
               WHERE strftime('%Y-%m', expense_date) = ? AND status = 'completed'""",
            (month,)
        )
        total_expenses = expenses_result['total_expenses'] if expenses_result else 0.0
        
        balance = total_income - total_expenses
        
        print(f"\n📊 BALANCE MENSUAL - {month}")
        print("=" * 40)
        print(f"Ingresos por retiros: ${total_income:,.2f}")
        print(f"Gastos totales:      ${total_expenses:,.2f}")
        print(f"Balance neto:        ${balance:,.2f}")
        print("=" * 40)
        
        if detailed:
            print("\n📋 DETALLE DE RETIROS:")
            withdrawals = db_manager.fetchall(
                """SELECT e.name as entity_name, g.name as genetic_name, 
                          w.grams, w.total_amount, w.withdrawal_date
                   FROM withdrawals w
                   JOIN entities e ON w.entity_id = e.id
                   JOIN genetics g ON w.genetic_id = g.id
                   WHERE strftime('%Y-%m', w.withdrawal_date) = ? AND w.status = 'completed'
                   ORDER BY w.withdrawal_date""",
                (month,)
            )
            
            for w in withdrawals:
                print(f"  {w['withdrawal_date']} - {w['entity_name']}: {w['grams']}g de {w['genetic_name']} - ${w['total_amount']:,.2f}")
            
            print("\n📋 DETALLE DE GASTOS:")
            expenses = db_manager.fetchall(
                """SELECT e.name as entity_name, c.name as concept_name, 
                          exp.amount, exp.expense_date, exp.folio
                   FROM expenses exp
                   JOIN entities e ON exp.entity_id = e.id
                   JOIN concepts c ON exp.concept_id = c.id
                   WHERE strftime('%Y-%m', exp.expense_date) = ? AND exp.status = 'completed'
                   ORDER BY exp.expense_date""",
                (month,)
            )
            
            for exp in expenses:
                folio_info = f" - Folio: {exp['folio']}" if exp['folio'] else ""
                print(f"  {exp['expense_date']} - {exp['entity_name']}: {exp['concept_name']} - ${exp['amount']:,.2f}{folio_info}")
                
    except Exception as e:
        logger.error(f"Error generando reporte de balance: {e}")
        raise

def generate_stock_report(genetic_filter: Optional[str] = None):
    """Generar reporte de stock actual"""
    try:
        query = """
            SELECT g.id, g.name, 
                   COALESCE(SUM(CASE WHEN sm.movement_type = 'in' THEN sm.quantity ELSE 0 END), 0) -
                   COALESCE(SUM(CASE WHEN sm.movement_type = 'out' THEN sm.quantity ELSE 0 END), 0) as available_stock
            FROM genetics g
            LEFT JOIN stock_movements sm ON g.id = sm.genetic_id
            WHERE g.status = 'active'
        """
        params = ()
        
        if genetic_filter:
            if genetic_filter.isdigit():
                query += " AND g.id = ?"
                params = (int(genetic_filter),)
            else:
                query += " AND g.name LIKE ?"
                params = (f"%{genetic_filter}%",)
        
        query += " GROUP BY g.id, g.name ORDER BY available_stock DESC"
        
        stock_data = db_manager.fetchall(query, params)
        
        print(f"\n📦 REPORTE DE STOCK - {datetime.now().strftime('%Y-%m-%d')}")
        print("=" * 50)
        total_stock = 0.0
        
        for item in stock_data:
            print(f"  {item['name']}: {item['available_stock']:,.2f}g")
            total_stock += item['available_stock']
        
        print("=" * 50)
        print(f"  TOTAL STOCK: {total_stock:,.2f}g")
        
    except Exception as e:
        logger.error(f"Error generando reporte de stock: {e}")
        raise