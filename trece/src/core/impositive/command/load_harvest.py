import csv
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from .db import db_manager

logger = logging.getLogger(__name__)

def load_harvest_from_csv(file_path: Path):
    """Cargar cosechas desde archivo CSV - AHORA SOPORTA MÚLTIPLES GENÉTICAS"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            harvests_data = list(reader)
        
        # Agrupar por cosecha (mismo harvest_date + module)
        harvests_grouped = {}
        for row in harvests_data:
            key = (row['harvest_date'], row['module'], row['genetic'])
            if key not in harvests_grouped:
                harvests_grouped[key] = []
            harvests_grouped[key].append(row)
        
        success_count = 0
        for (harvest_date, module_name), genetics_data in harvests_grouped.items():
            try:
                create_harvest_with_multiple_genetics(
                    harvest_date=harvest_date,
                    module_name=module_name,
                    genetics_data=genetics_data
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Error creando cosecha {harvest_date} - {module_name}: {e}")
        
        logger.info(f"✅ Cargadas {success_count} cosechas con {len(harvests_data)} items desde {file_path}")
        
    except Exception as e:
        logger.error(f"Error cargando archivo CSV: {e}")
        raise

# ✅ NUEVA FUNCIÓN PARA MÚLTIPLES GENÉTICAS
def create_harvest_with_multiple_genetics(
    harvest_date: str,
    module_name: str,
    genetics_data: List[Dict],  # Lista de diccionarios con 'genetic' y 'grams'
    quality_notes: str = None
):
    """Crear una cosecha con múltiples genéticas"""
    
    module_id = _get_or_create_module(module_name)
    total_grams = sum(float(item['grams']) for item in genetics_data)
    
    # Usar las notas de calidad del primer item si no se especifican
    if not quality_notes and genetics_data:
        quality_notes = genetics_data[0].get('quality_notes')
    
    # Crear la cosecha principal
    harvest_id = db_manager.insert_and_get_id(
        """INSERT INTO harvests 
           (module_id, harvest_date, total_grams, notes, status)
           VALUES (?, ?, ?, ?, ?)""",
        (module_id, harvest_date, total_grams, quality_notes, 'completed')
    )
    
    # Crear múltiples items de cosecha
    for genetic_item in genetics_data:
        genetic_name = genetic_item['genetic']
        grams = float(genetic_item['grams'])
        genetic_id = _get_genetic_id(genetic_name)
        
        # Crear item de cosecha para esta genética
        db_manager.insert_and_get_id(
            """INSERT INTO harvest_items 
               (harvest_id, genetic_id, grams, quality_notes)
               VALUES (?, ?, ?, ?)""",
            (harvest_id, genetic_id, grams, quality_notes)
        )
        
        # Registrar movimiento de stock
        db_manager.insert_and_get_id(
            """INSERT INTO stock_movements 
               (genetic_id, movement_type, quantity, reference_table, reference_id, movement_date)
               VALUES (?, 'in', ?, 'harvest_items', ?, ?)""",
            (genetic_id, grams, harvest_id, harvest_date)
        )
        
        logger.info(f"  ✅ {grams}g de {genetic_name}")
    
    logger.info(f"✅ Cosecha {harvest_date} - {module_name}: {len(genetics_data)} genéticas, {total_grams}g total")
    return harvest_id

# ✅ MANTENER función original para compatibilidad
def create_harvest(
    genetic_name: str,
    grams: float,
    harvest_date: str,
    module_name: str,
    quality_notes: str = None
):
    """Crear una cosecha con una sola genética (para compatibilidad con CLI)"""
    return create_harvest_with_multiple_genetics(
        harvest_date=harvest_date,
        module_name=module_name,
        genetics_data=[{'genetic': genetic_name, 'grams': grams}],
        quality_notes=quality_notes
    )

def _get_genetic_id(genetic_name: str) -> int:
    """Obtener ID de genética por nombre"""
    result = db_manager.fetchone(
        "SELECT id FROM genetics WHERE name = ?",
        (genetic_name,)
    )
    if not result:
        raise ValueError(f"Genética '{genetic_name}' no encontrada")
    return result['id']

def _get_or_create_module(module_name: str) -> int:
    """Obtener o crear módulo por nombre"""
    result = db_manager.fetchone(
        "SELECT id FROM modules WHERE name = ?",
        (module_name,)
    )
    if result:
        return result['id']
    
    # Crear nuevo módulo
    return db_manager.insert_and_get_id(
        "INSERT INTO modules (name, description) VALUES (?, ?)",
        (module_name, f"Módulo {module_name}")
    )