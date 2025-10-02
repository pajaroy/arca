import csv
import logging
from pathlib import Path
from typing import List, Dict, Any
from .db import db_manager

logger = logging.getLogger(__name__)

def load_genetics_from_csv(file_path: Path):
    """Cargar genéticas desde archivo CSV"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            genetics = list(reader)
        
        success_count = 0
        for genetic_data in genetics:
            try:
                create_genetic(
                    name=genetic_data['name'],
                    description=genetic_data.get('description'),
                    thc_range=genetic_data.get('thc_range'),
                    cbd_range=genetic_data.get('cbd_range'),
                    flowering_days=genetic_data.get('flowering_days')
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Error creando genética {genetic_data['name']}: {e}")
        
        logger.info(f"✅ Cargadas {success_count}/{len(genetics)} genéticas desde {file_path}")
        
    except Exception as e:
        logger.error(f"Error cargando archivo CSV: {e}")
        raise

def create_genetic(
    name: str,
    description: str = None,
    thc_range: str = None,
    cbd_range: str = None,
    flowering_days: int = None
):
    """Crear una genética directamente"""
    # Verificar si la genética ya existe
    existing = db_manager.fetchone(
        "SELECT id FROM genetics WHERE name = ?",
        (name,)
    )
    
    if existing:
        logger.warning(f"Genética '{name}' ya existe")
        return existing['id']
    
    # Crear nueva genética
    genetic_id = db_manager.insert_and_get_id(
        """INSERT INTO genetics 
           (name, description, thc_range, cbd_range, flowering_days)
           VALUES (?, ?, ?, ?, ?)""",
        (name, description, thc_range, cbd_range, flowering_days)
    )
    
    logger.info(f"✅ Genética '{name}' creada con ID {genetic_id}")
    return genetic_id