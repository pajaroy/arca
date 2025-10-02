import csv
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from .db import db_manager

logger = logging.getLogger(__name__)

def load_withdrawal_from_csv(file_path: Path):
    """Cargar retiros desde archivo CSV - AHORA SOPORTA PRECIOS DIFERENCIADOS"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            withdrawals = list(reader)
        
        success_count = 0
        for withdrawal_data in withdrawals:
            try:
                # ✅ CAMBIAR: Agregar price_type al CSV
                create_withdrawal(
                    entity_name=withdrawal_data['entity'],
                    genetic_name=withdrawal_data['genetic'],
                    grams=float(withdrawal_data['grams']),
                    withdrawal_date=withdrawal_data['withdrawal_date'],
                    price_type=withdrawal_data.get('price_type'),  # ← NUEVO
                    price_per_gram=float(withdrawal_data.get('price_per_gram', 0)),
                    notes=withdrawal_data.get('notes')
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Error creando retiro: {e}")
        
        logger.info(f"✅ Cargados {success_count}/{len(withdrawals)} retiros desde {file_path}")
        
    except Exception as e:
        logger.error(f"Error cargando archivo CSV: {e}")
        raise

def create_withdrawal(
    entity_name: str,
    genetic_name: str,
    grams: float,
    withdrawal_date: str,
    price_type: str = None,           # ← NUEVO PARÁMETRO
    price_per_gram: float = None,
    notes: str = None
):
    """Crear un retiro directamente - AHORA SOPORTA PRECIOS DIFERENCIADOS"""
    # ✅ CAMBIAR: Obtener entity_id sin tipo fijo
    entity_id = _get_entity_id(entity_name)  # ← QUITAR 'socio'
    genetic_id = _get_genetic_id(genetic_name)
    
    # ✅ NUEVO: Determinar tipo de precio automáticamente
    if not price_type:
        price_type = _detect_price_type(entity_id)
    
    # Validar stock disponible
    available_stock = get_available_stock(genetic_id)
    if available_stock < grams:
        raise ValueError(f"Stock insuficiente. Disponible: {available_stock}g, Solicitado: {grams}g")
    
    # ✅ CAMBIAR: Obtener precio según tipo
    if not price_per_gram:
        price_per_gram = get_current_price(genetic_id, price_type)  # ← AGREGAR price_type
    
    total_amount = grams * price_per_gram
    
    # Crear el retiro
    withdrawal_id = db_manager.insert_and_get_id(
        """INSERT INTO withdrawals 
           (entity_id, genetic_id, grams, price_per_gram, total_amount, withdrawal_date, notes, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (entity_id, genetic_id, grams, price_per_gram, total_amount, withdrawal_date, notes, 'completed')
    )
    
    # Registrar movimiento de stock
    db_manager.insert_and_get_id(
        """INSERT INTO stock_movements 
           (genetic_id, movement_type, quantity, reference_table, reference_id, movement_date)
           VALUES (?, 'out', ?, 'withdrawals', ?, ?)""",
        (genetic_id, grams, withdrawal_id, withdrawal_date)
    )
    
    # ✅ CAMBIAR: Log con tipo de precio
    tipo_str = "socio" if price_type == 'retail' else "mayorista"
    logger.info(f"✅ Retiro {tipo_str}: {grams}g de {genetic_name} para {entity_name} - ${total_amount:,.2f}")
    return withdrawal_id

# ✅ CAMBIAR: Quitar entity_type fijo
def _get_entity_id(entity_name: str) -> int:  # ← QUITAR entity_type
    """Obtener ID de entidad por nombre (cualquier tipo)"""
    result = db_manager.fetchone(
        "SELECT id FROM entities WHERE name = ?",  # ← QUITAR filtro por tipo
        (entity_name,)
    )
    if not result:
        raise ValueError(f"Entidad '{entity_name}' no encontrada")
    return result['id']

# ✅ NUEVA FUNCIÓN: Detectar tipo de precio
def _detect_price_type(entity_id: int) -> str:
    """Detectar tipo de precio basado en tipo de entidad"""
    result = db_manager.fetchone(
        """SELECT et.name as entity_type 
           FROM entities e 
           JOIN entity_types et ON e.entity_type_id = et.id 
           WHERE e.id = ?""",
        (entity_id,)
    )
    
    if result and result['entity_type'] == 'mayorista':
        return 'wholesale'
    else:
        return 'retail'

def _get_genetic_id(genetic_name: str) -> int:
    """Obtener ID de genética por nombre"""
    result = db_manager.fetchone(
        "SELECT id FROM genetics WHERE name = ?",
        (genetic_name,)
    )
    if not result:
        raise ValueError(f"Genética '{genetic_name}' no encontrada")
    return result['id']

def get_available_stock(genetic_id: int) -> float:
    """Obtener stock disponible para una genética"""
    result = db_manager.fetchone(
        """SELECT 
               COALESCE(SUM(CASE WHEN movement_type = 'in' THEN quantity ELSE 0 END), 0) -
               COALESCE(SUM(CASE WHEN movement_type = 'out' THEN quantity ELSE 0 END), 0) as available
           FROM stock_movements 
           WHERE genetic_id = ?""",
        (genetic_id,)
    )
    return result['available'] if result else 0.0

# ✅ CAMBIAR: Agregar soporte para price_type
def get_current_price(genetic_id: int, price_type: str = 'retail') -> float:
    """Obtener precio actual de una genética por tipo"""
    result = db_manager.fetchone(
        """SELECT price_per_gram FROM prices 
           WHERE genetic_id = ? AND price_type = ?
           AND (end_date IS NULL OR end_date >= DATE('now'))
           ORDER BY start_date DESC LIMIT 1""",
        (genetic_id, price_type)
    )
    if not result:
        if price_type == 'wholesale':
            return get_current_price(genetic_id, 'retail')
        raise ValueError(f"No hay precio {price_type} definido para la genética ID {genetic_id}")
    return result['price_per_gram']