# alma_core/core/notebooks/llm_server_v0.1.0/main.py
import argparse
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional

# Importaciones de módulos de integración
from integration.schemas import AlmaBaseModel, generate_hash
from integration.context_tracker import ContextTracker
from integration.memory_graph import MemoryGraph
from integration.model_wrapper import ModelWrapper

# Configuración centralizada de logging
from integration.logging_config import configure_logging

configure_logging()
logger = logging.getLogger('llm_server_main')

class LLMRequest(AlmaBaseModel):
    """Esquema universal para solicitudes al LLM Server"""
    prompt: str
    metadata: Dict = Field(default_factory=dict)
    memoria_ref: List[str] = Field(default_factory=list)

class LLMResponse(AlmaBaseModel):
    """Esquema universal para respuestas del LLM Server"""
    respuesta: str
    metadata: Dict = Field(default_factory=dict)
    memoria_ref: List[str] = Field(default_factory=list)

class LLMServer:
    def __init__(self):
        self.context_tracker = ContextTracker()
        self.memory_graph = MemoryGraph()
        self.model_wrapper = ModelWrapper()
        self.audit_log = []
        logger.info("LLM Server iniciado - ALMA_RESIST v0.2")

    def process_request(self, request_data: dict) -> dict:
        """Procesa una solicitud completa validando todos los campos universales"""
        # Validación estricta del request
        request = self._validate_request(request_data)
        
        # Registrar en contexto y memoria
        context_id = self.context_tracker.add_interaction(
            **request.dict(),
            response="",  # Respuesta pendiente
            tags=request.tags
        )
        
        # Generar respuesta del modelo
        model_response = self.model_wrapper.generate(
            **request.dict(),
            respuesta=""  # Valor temporal
        )
        
        # Construir respuesta final
        response = LLMResponse(
            **model_response.dict(),
            metadata={
                **model_response.metadata,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Actualizar contexto con respuesta real
        self.context_tracker.history[-1].response = response.respuesta
        
        # Registrar en grafo de memoria
        node_id = self.memory_graph.add_node(
            id=f"NODE_{datetime.utcnow().strftime('%Y-%m-%d_%H%M%S')}",
            agente=request.agente,
            concepto=request.prompt[:50] + "...",
            tags=request.tags,
            metadata={
                "tipo": "interacción",
                "respuesta_hash": generate_hash(response.respuesta)
            },
            memoria_ref=request.memoria_ref
        )
        
        self._audit("REQUEST_PROCESSED", request.id, response.id)
        return response.dict()

    def _validate_request(self, data: dict) -> LLMRequest:
        """Validación estricta con esquemas universales"""
        required_fields = {'id', 'agente', 'prompt', 'hash'}
        if not required_fields.issubset(data.keys()):
            missing = required_fields - set(data.keys())
            raise ValueError(f"Campos obligatorios faltantes: {missing}")
        
        # Verificar integridad del hash
        data_copy = data.copy()
        provided_hash = data_copy.pop('hash', None)
        computed_hash = generate_hash(data_copy)
        
        if provided_hash != computed_hash:
            raise ValueError("Fallo de integridad: hash no coincide")
        
        return LLMRequest(**data)

    def query_context(
        self,
        agent: Optional[str] = None,
        tags: Optional[List[str]] = None,
        date_range: Optional[tuple] = None
    ) -> List[dict]:
        """Consulta el historial de interacciones"""
        return self.context_tracker.query(agent, tags, date_range)

    def query_graph(
        self,
        concept: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[dict]:
        """Consulta el grafo de memoria"""
        return self.memory_graph.query(concept, tags)

    def health_check(self) -> Dict[str, str]:
        """Verifica el estado del sistema"""
        return {
            "status": "OPERATIONAL",
            "components": {
                "context_tracker": f"{len(self.context_tracker.history)} registros",
                "memory_graph": f"{self.memory_graph.graph.number_of_nodes()} nodos",
                "model_wrapper": "ACTIVE"
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    def export_data(self, format: str = "json") -> str:
        """Exporta datos en formato compatible"""
        # Implementación simplificada
        return json.dumps({
            "context": [r.dict() for r in self.context_tracker.history],
            "memory_graph": list(self.memory_graph.graph.nodes(data=True))
        })

    def _audit(self, action: str, request_id: str, response_id: str):
        """Registro de auditoría estructurado"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "request_id": request_id,
            "response_id": response_id,
            "system_state": self.health_check()
        }
        self.audit_log.append(entry)
        logger.info(f"AUDIT | {action} | Req:{request_id} | Res:{response_id}")

# CLI Implementation
def main():
    server = LLMServer()
    parser = argparse.ArgumentParser(description="LLM Server CLI - ALMA_RESIST v0.2")
    
    subparsers = parser.add_subparsers(dest='command')
    
    # Parser para solicitudes
    request_parser = subparsers.add_parser('request')
    request_parser.add_argument('--id', required=True, help="ID único de solicitud")
    request_parser.add_argument('--agente', required=True, help="Agente solicitante")
    request_parser.add_argument('--prompt', required=True, help="Prompt de entrada")
    request_parser.add_argument('--tags', nargs='+', default=[], help="Etiquetas")
    request_parser.add_argument('--memoria_ref', nargs='+', default=[], help="Referencias a memoria")
    request_parser.add_argument('--metadata', type=json.loads, default={}, help="Metadatos en JSON")
    
    # Comandos de consulta
    subparsers.add_parser('context')
    subparsers.add_parser('graph')
    subparsers.add_parser('health')
    subparsers.add_parser('export')
    
    args = parser.parse_args()
    
    if args.command == "request":
        # Generar hash automático
        data = vars(args)
        data['hash'] = generate_hash({
            k: v for k, v in data.items() if k != 'command'
        })
        
        response = server.process_request(data)
        print(json.dumps(response, indent=2))
    
    elif args.command == "context":
        print(json.dumps(server.query_context(), indent=2))
    
    elif args.command == "graph":
        print(json.dumps(server.query_graph(), indent=2))
    
    elif args.command == "health":
        print(json.dumps(server.health_check(), indent=2))
    
    elif args.command == "export":
        print(server.export_data())

if __name__ == "__main__":
    main()