
# access_control.py
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def verificar_acceso(memoria: dict, user_id: str, rol: str) -> bool:
    """
    Verifica si un usuario tiene permiso para acceder a una memoria según su visibilidad.
    
    Args:
        memoria (dict): Diccionario con la memoria a verificar
        user_id (str): Identificador del usuario solicitante
        rol (str): Rol del usuario en el sistema
    
    Returns:
        bool: True si tiene acceso, False en caso contrario
    """
    visibilidad = memoria.get('visibilidad')
    
    if visibilidad == "publica":
        return True
    elif visibilidad == "privada":
        return user_id == memoria.get('owner_id')
    elif visibilidad == "solo_sistema":
        return rol == "sistema"
    return False

def registrar_traza(evento: str, memoria_id: str, user_id: str = None, metadata: dict = None):
    """
    Registra un evento de acceso en logs estructurados.
    
    Args:
        evento (str): Tipo de evento (ej: "acceso_denegado", "acceso_exitoso")
        memoria_id (str): Identificador de la memoria accedida
        user_id (str, opcional): ID del usuario relacionado
        metadata (dict, opcional): Metadatos adicionales del evento
    """
    traza = {
        "evento": evento,
        "memoria_id": memoria_id,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if metadata:
        traza.update(metadata)
    
    # Log estructurado compatible con sistemas de monitoreo
    logger.info(
        "Evento de trazabilidad registrado",
        extra={"traza": traza}
    )
