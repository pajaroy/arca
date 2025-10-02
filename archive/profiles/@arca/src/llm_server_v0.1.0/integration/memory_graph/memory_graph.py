from schemas import AlmaBaseModel
import networkx as nx
import logging

class MemoryNode(AlmaBaseModel):
    concepto: str

class MemoryGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.logger = logging.getLogger('memory_graph')

    def add_node(self, **kwargs):
        node = MemoryNode(**kwargs)
        self.graph.add_node(node.id, **node.dict())
        self._audit("ADD_NODE", node)
        return node.id

    def add_edge(self, source_id: str, target_id: str, relationship: str):
        if source_id in self.graph and target_id in self.graph:
            self.graph.add_edge(source_id, target_id, label=relationship)
            self._audit("ADD_EDGE", f"{source_id} -> {target_id} [{relationship}]")
    
    def query(self, concept: Optional[str] = None, tags: Optional[List[str]] = None):
        results = []
        for node_id, data in self.graph.nodes(data=True):
            if concept and concept.lower() not in data['concepto'].lower():
                continue
            if tags and not any(t in data['tags'] for t in tags):
                continue
            results.append(data)
        return results

    def _audit(self, action: str, data):
        log_msg = f"{action} | {data}"
        self.logger.info(log_msg)

# Ejemplo de uso:
# graph = MemoryGraph()
# node_id = graph.add_node(
#     id="NODE_2025-06-11_002",
#     agente="centralesis",
#     concepto="memoria viva",
#     tags=["concepto", "ALMA"],
#     metadata={"relaciones": ["RAG"]},
#     memoria_ref=["MEM_2025-06-11_09"]
# )
# graph.add_edge("NODE_2025-06-11_002", "CTX_2025-06-11_001", "relacionado")