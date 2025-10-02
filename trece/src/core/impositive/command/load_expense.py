import csv
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from .db import db_manager

logger = logging.getLogger(__name__)

def load_expense_from_csv(file_path: Path):
    """Cargar gastos desde archivo CSV"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
        
        success_count = 0
        for expense_data in expenses:
            try:
                create_expense(
                    entity_name=expense_data['entity'],
                    amount=float(expense_data['amount']),
                    concept_name=expense_data['concept'],
                    expense_date=expense_data['expense_date'],
                    folio=expense_data.get('folio'),
                    paymethod_name=expense_data.get('paymethod', 'efectivo'),
                    notes=expense_data.get('notes')
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Error creando gasto: {e}")
        
        logger.info(f"✅ Cargados {success_count}/{len(expenses)} gastos desde {file_path}")
        
    except Exception as e:
        logger.error(f"Error cargando archivo CSV: {e}")
        raise

def create_expense(
    entity_name: str,
    amount: float,
    concept_name: str,
    expense_date: str,
    folio: str = None,
    paymethod_name: str = 'efectivo',
    notes: str = None
):
    """Crear un gasto directamente"""
    # Obtener IDs por nombre
    entity_id = _get_entity_id(entity_name, 'proveedor')
    concept_id = _get_or_create_concept(concept_name)
    paymethod_id = _get_paymethod_id(paymethod_name)
    
    # Crear el gasto
    expense_id = db_manager.insert_and_get_id(
        """INSERT INTO expenses 
           (entity_id, concept_id, amount, expense_date, folio, paymethod_id, notes, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (entity_id, concept_id, amount, expense_date, folio, paymethod_id, notes, 'completed')
    )
    
    logger.info(f"✅ Gasto de ${amount} para {entity_name} registrado")
    return expense_id

def _get_entity_id(entity_name: str, entity_type: str) -> int:
    """Obtener ID de entidad por nombre y tipo"""
    result = db_manager.fetchone(
        """SELECT e.id FROM entities e 
           JOIN entity_types et ON e.entity_type_id = et.id 
           WHERE e.name = ? AND et.name = ?""",
        (entity_name, entity_type)
    )
    if not result:
        raise ValueError(f"Entidad '{entity_name}' de tipo '{entity_type}' no encontrada")
    return result['id']

def _get_or_create_concept(concept_name: str) -> int:
    """Obtener o crear concepto por nombre"""
    result = db_manager.fetchone(
        "SELECT id FROM concepts WHERE name = ?",
        (concept_name.lower(),)
    )
    if result:
        return result['id']
    
    # Crear nuevo concepto
    return db_manager.insert_and_get_id(
        "INSERT INTO concepts (name, description) VALUES (?, ?)",
        (concept_name.lower(), f"Concepto: {concept_name}")
    )

def _get_paymethod_id(paymethod_name: str) -> int:
    """Obtener ID de método de pago por nombre"""
    result = db_manager.fetchone(
        "SELECT id FROM paymethods WHERE name = ?",
        (paymethod_name.lower(),)
    )
    if not result:
        raise ValueError(f"Método de pago '{paymethod_name}' no encontrado")
    return result['id']