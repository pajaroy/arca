from schemas import AlmaBaseModel
import logging

class InteractionRecord(AlmaBaseModel):
    prompt: str
    response: str

class ContextTracker:
    def __init__(self):
        self.history: List[InteractionRecord] = []
        self.logger = logging.getLogger('context_tracker')

    def add_interaction(self, **kwargs):
        record = InteractionRecord(**kwargs)
        self.history.append(record)
        self._audit("ADD", record)
        return record.id

    def query(self, agent: Optional[str] = None, tags: Optional[List[str]] = None):
        results = self.history
        if agent: results = [r for r in results if r.agente == agent]
        if tags: results = [r for r in results if any(t in r.tags for t in tags)]
        return results

    def _audit(self, action: str, record: InteractionRecord):
        log_msg = f"{action} | ID:{record.id} | Agente:{record.agente} | Hash:{record.hash[:8]}"
        self.logger.info(log_msg)

# Ejemplo de uso:
# tracker = ContextTracker()
# tracker.add_interaction(
#     id="CTX_2025-06-11_001",
#     agente="kael",
#     prompt="¿Qué es memoria institucional?",
#     response="Sistema centralizado de conocimiento...",
#     tags=["memoria", "ALMA"],
#     metadata={"model": "Mistral-7B"},
#     memoria_ref=["MEM_2025-06-11_09"]
# )