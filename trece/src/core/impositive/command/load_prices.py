import csv
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from .db import db_manager

logger = logging.getLogger(__name__)

def load_prices_from_csv(file_path: Path):
    """Cargar precios desde archivo CSV"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            prices = list(reader)
        
        success_count = 0
        for price_data in prices:
            try:
                create_price(
                    genetic_name=price_data['genetic'],
                    price_per_gram=float(price_data['price_per_gram']),
                    price_type=price_data.get('price_type', 'retail'),
                    start_date=price_data.get('start_date', datetime.now().strftime('%Y-%m-%d'))
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Error creando precio: {e}")
        
        logger.info(f"✅ Cargados {success_count}/{len(prices)} precios desde {file_path}")
        
    except Exception as e:
        logger.error(f"Error cargando archivo CSV: {e}")
        raise

def create_price(
    genetic_name: str,
    price_per_gram: float,
    price_type: str = 'retail',
    start_date: str = None
):
    """Crear un precio directamente"""
    if not start_date:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    # Validar tipo de precio
    if price_type not in ['retail', 'wholesale']:
        raise ValueError("price_type debe ser 'retail' o 'wholesale'")
    
    genetic_id = _get_genetic_id(genetic_name)
    
    # Cerrar precio anterior del mismo tipo
    db_manager.execute(
        "UPDATE prices SET end_date = ? WHERE genetic_id = ? AND price_type = ? AND end_date IS NULL",
        (start_date, genetic_id, price_type)
    )
    
    # Crear nuevo precio
    price_id = db_manager.insert_and_get_id(
        """INSERT INTO prices 
           (genetic_id, price_per_gram, price_type, start_date)
           VALUES (?, ?, ?, ?)""",
        (genetic_id, price_per_gram, price_type, start_date)
    )
    
    tipo_str = "socio" if price_type == 'retail' else "mayorista"
    logger.info(f"✅ Precio {tipo_str}: ${price_per_gram}/g para {genetic_name}")
    return price_id

def _get_genetic_id(genetic_name: str) -> int:
    """Obtener ID de genética por nombre"""
    result = db_manager.fetchone(
        "SELECT id FROM genetics WHERE name = ?",
        (genetic_name,)
    )
    if not result:
        raise ValueError(f"Genética '{genetic_name}' no encontrada")
    return result['id']