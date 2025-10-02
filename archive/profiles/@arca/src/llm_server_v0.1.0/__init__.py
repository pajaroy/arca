# Módulo principal del servidor LLM - ALMA_RESIST
# Exporta los componentes clave para integración y testing.

# Módulos principales
from . import model_wrapper
from . import transport_layer
from . import main

# Submódulos de integración
from .integration import context_tracker
from .integration import memory_graph

# Utilidades
from .utils import log_crypto
from .utils import log_writer

__all__ = [
    # Módulos base
    "model_wrapper",
    "transport_layer",
    "main",

    # Integraciones
    "context_tracker",
    "memory_graph",

    # Utilidades
    "log_crypto",
    "log_writer"
]

# Metadatos del paquete
__version__ = "0.0.0.4.1"
__author__ = "Equipo ALMA_RESIST"
