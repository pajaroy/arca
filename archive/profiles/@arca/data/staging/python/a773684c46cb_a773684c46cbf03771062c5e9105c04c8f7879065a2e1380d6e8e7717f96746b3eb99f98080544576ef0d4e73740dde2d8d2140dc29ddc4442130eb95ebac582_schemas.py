from pydantic import BaseModel, Field, validator
from datetime import datetime
import hashlib
import json
from typing import Dict, List, Optional

def generate_hash(data: dict) -> str:
    """Genera hash SHA-256 de datos serializados canónicamente"""
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return f"sha256:{hashlib.sha256(canonical.encode()).hexdigest()}"

class AlmaBaseModel(BaseModel):
    id: str
    agente: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)
    hash: str
    metadata: Dict = Field(default_factory=dict)
    memoria_ref: List[str] = Field(default_factory=list)

    @validator('hash', pre=True, always=True)
    def compute_hash(cls, v, values):
        if v: return v
        data = values.copy()
        if 'hash' in data: del data['hash']
        return generate_hash(data)