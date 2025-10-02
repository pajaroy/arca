import logging
import os
import json
from python_json_logger import JSONFormatter
from logging.handlers import TimedRotatingFileHandler
from . import log_crypto, log_writer

# Environment variables
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
ENABLE_ENCRYPTION = os.getenv("LOG_ENCRYPTION_ENABLED", "false").lower() == "true"
LOG_DIR = os.getenv("LOG_DIR", "logs")

class AlmaJSONFormatter(JSONFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        # Ensure universal fields exist
        log_record.setdefault('id', "N/A")
        log_record.setdefault('agente', "unknown")
        log_record.setdefault('hash', "N/A")
        log_record.setdefault('memoria_ref', [])
        log_record.setdefault('tags', [])
        log_record.setdefault('metadata', {})

def configure_logging(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(LOG_LEVEL)

    # Create log directory if missing
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"{module_name}.log")

    # File handler with rotation
    handler = TimedRotatingFileHandler(
        log_file,
        when='midnight',
        backupCount=7,
        encoding='utf-8'
    )
    handler.setFormatter(AlmaJSONFormatter())
    
    # Encryption hook for CRITICAL logs
    if ENABLE_ENCRYPTION:
        class EncryptionFilter(logging.Filter):
            def filter(self, record):
                if record.levelno >= logging.CRITICAL:
                    record.msg = log_crypto.encrypt_log(record.msg)
                return True
        handler.addFilter(EncryptionFilter())
    
    logger.addHandler(handler)
    
    # Register rotator for encrypted backups
    handler.namer = log_writer.encrypted_namer if ENABLE_ENCRYPTION else None
    handler.rotator = log_writer.log_rotator
    
    return logger