import csv
import logging
from pathlib import Path
from typing import List, Dict, Any
from .db import db_manager

logger = logging.getLogger(__name__)

def load_entities_from_csv(file_path: Path):
    """Cargar entidades desde archivo CSV"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            entities = list(reader)
        
        success_count = 0
        for entity_data in entities:
            try:
                create_entity(
                    name=entity_data['name'],
                    entity_type=entity_data['entity_type'],
                    email=entity_data.get('email'),
                    phone=entity_data.get('phone'),
                    address=entity_data.get('address'),
                    membership_number=entity_data.get('membership_number')
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Error creando entidad {entity_data['name']}: {e}")
        
        logger.info(f"✅ Cargadas {success_count}/{len(entities)} entidades desde {file_path}")
        
    except Exception as e:
        logger.error(f"Error cargando archivo CSV: {e}")
        raise

def create_entity(
    name: str,
    entity_type: str,
    email: str = None,
    phone: str = None,
    address: str = None,
    membership_number: str = None
):
    """Crear una entidad directamente"""
    # Obtener o crear el tipo de entidad
    entity_type_id = _get_or_create_entity_type(entity_type)
    
    # Verificar si la entidad ya existe
    existing = db_manager.fetchone(
        "SELECT id FROM entities WHERE name = ? AND entity_type_id = ?",
        (name, entity_type_id)
    )
    
    if existing:
        logger.warning(f"Entidad '{name}' ({entity_type}) ya existe")
        return existing['id']
    
    # Crear nueva entidad
    entity_id = db_manager.insert_and_get_id(
        """INSERT INTO entities 
           (name, entity_type_id, email, phone, address, membership_number)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (name, entity_type_id, email, phone, address, membership_number)
    )
    
    logger.info(f"✅ Entidad '{name}' creada con ID {entity_id}")
    return entity_id

def _get_or_create_entity_type(entity_type_name: str) -> int:
    """Obtener ID de tipo de entidad o crearlo si no existe"""
    result = db_manager.fetchone(
        "SELECT id FROM entity_types WHERE name = ?",
        (entity_type_name.lower(),)
    )
    
    if result:
        return result['id']
    
    # Crear nuevo tipo de entidad
    return db_manager.insert_and_get_id(
        "INSERT INTO entity_types (name) VALUES (?)",
        (entity_type_name.lower(),)
    )