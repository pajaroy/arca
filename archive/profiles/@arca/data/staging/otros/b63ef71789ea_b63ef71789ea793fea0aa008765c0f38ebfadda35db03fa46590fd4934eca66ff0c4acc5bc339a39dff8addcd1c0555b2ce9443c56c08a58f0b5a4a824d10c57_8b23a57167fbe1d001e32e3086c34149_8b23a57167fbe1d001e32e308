from pydantic import BaseModel, Field, validator
from datetime import datetime
import hashlib
from .logging_config import configure_logger
import json

logger = configure_logger("transport_layer")

class UniversalSchema(BaseModel):
    id: str = Field(..., min_length=8)
    agente: str
    timestamp: str  # ISO 8601
    tags: list[str] = []
    hash: str
    metadata: dict = {}
    memoria_ref: list[str] = []

    @validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Invalid ISO 8601 timestamp")

    @validator('hash')
    def validate_hash(cls, v, values):
        data_str = f"{values['id']}{values['agente']}{values['timestamp']}"
        expected = hashlib.sha256(data_str.encode()).hexdigest()
        if v != expected:
            raise ValueError("Hash validation failed")
        return v

def log_transport(data: dict):
    """Process and validate transport data with audit logging"""
    try:
        validated = UniversalSchema(**data)
        audit_log = validated.dict()
        logger.info(
            "Transport validated", 
            extra=audit_log,
            stack_info=True
        )
        return validated
    except Exception as e:
        logger.critical(
            "Transport validation failed",
            extra={
                "id": data.get("id", "UNKNOWN"),
                "agente": data.get("agente", "system"),
                "error": str(e),
                "original_data": json.dumps(data)
            }
        )
        raise

# Example usage:
if __name__ == "__main__":
    sample_data = {
        "id": "req_12345",
        "agente": "llm_gateway",
        "timestamp": datetime.utcnow().isoformat(),
        "hash": hashlib.sha256(b"req_12345llm_gateway").hexdigest(),
        "memoria_ref": ["ctx_67890"]
    }
    validated = log_transport(sample_data)