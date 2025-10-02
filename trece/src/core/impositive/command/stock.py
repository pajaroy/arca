import logging
from typing import List, Dict, Any
from .db import db_manager

logger = logging.getLogger(__name__)

def rebuild_stock():
    """Reconstruir movimientos de stock desde las tablas base"""
    try:
        logger.info("Iniciando reconstrucción de movimientos de stock...")
        
        # Limpiar movimientos existentes
        db_manager.execute("DELETE FROM stock_movements")
        logger.info("Movimientos de stock anteriores eliminados")
        
        # Reconstruir desde cosechas
        harvest_items = db_manager.fetchall("""
            SELECT hi.id, hi.harvest_id, hi.genetic_id, hi.grams, h.harvest_date
            FROM harvest_items hi
            JOIN harvests h ON hi.harvest_id = h.id
            WHERE h.status = 'completed'
        """)
        
        for item in harvest_items:
            db_manager.execute(
                """INSERT INTO stock_movements 
                   (genetic_id, movement_type, quantity, reference_table, reference_id, movement_date)
                   VALUES (?, 'in', ?, 'harvest_items', ?, ?)""",
                (item['genetic_id'], item['grams'], item['id'], item['harvest_date'])
            )
        
        logger.info(f"Registrados {len(harvest_items)} movimientos de entrada por cosechas")
        
        # Reconstruir desde retiros
        withdrawals = db_manager.fetchall("""
            SELECT id, genetic_id, grams, withdrawal_date
            FROM withdrawals 
            WHERE status = 'completed'
        """)
        
        for withdrawal in withdrawals:
            db_manager.execute(
                """INSERT INTO stock_movements 
                   (genetic_id, movement_type, quantity, reference_table, reference_id, movement_date)
                   VALUES (?, 'out', ?, 'withdrawals', ?, ?)""",
                (withdrawal['genetic_id'], withdrawal['grams'], withdrawal['id'], withdrawal['withdrawal_date'])
            )
        
        logger.info(f"Registrados {len(withdrawals)} movimientos de salida por retiros")
        
        total_movements = len(harvest_items) + len(withdrawals)
        logger.info(f"✅ Reconstrucción completada: {total_movements} movimientos registrados")
        
    except Exception as e:
        logger.error(f"Error reconstruyendo stock: {e}")
        raise

def get_stock_summary() -> List[Dict[str, Any]]:
    """Obtener resumen de stock por genética"""
    return db_manager.fetchall("""
        SELECT g.id, g.name, 
               COALESCE(SUM(CASE WHEN sm.movement_type = 'in' THEN sm.quantity ELSE 0 END), 0) as total_in,
               COALESCE(SUM(CASE WHEN sm.movement_type = 'out' THEN sm.quantity ELSE 0 END), 0) as total_out,
               COALESCE(SUM(CASE WHEN sm.movement_type = 'in' THEN sm.quantity ELSE 0 END), 0) -
               COALESCE(SUM(CASE WHEN sm.movement_type = 'out' THEN sm.quantity ELSE 0 END), 0) as available
        FROM genetics g
        LEFT JOIN stock_movements sm ON g.id = sm.genetic_id
        WHERE g.status = 'active'
        GROUP BY g.id, g.name
        ORDER BY available DESC
    """)