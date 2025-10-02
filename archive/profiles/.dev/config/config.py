# ---
# type: "script"
# date: "2025-08-22"
# version: "0.1.0"
# description: "configuracion base de modulo autonomo, version estable y autonoma"
# linked_to: ""
# changelog: ""
# ---
# config/config.py
from pathlib import Path
from datetime import date
import argparse

class Config:
    def __init__(self):
        # ruta base
        self.ROOT = Path(__file__).resolve().parent.parent
        self.__version__ = "0.1.0"
        self.AUTOR = "dev"

        # Archive
        self.ARCHIVE = self.ROOT / "archive"
        self.BACKUP = self.ARCHIVE / "backup"
        self.HISTORY = self.ARCHIVE / "history"

        # Config
        self.CONFIG = self.ROOT / "config"
        
        # Data
        self.DATA = self.ROOT / "data"
        self.BITACORA = self.DATA / "bitacora"
        self.INDEX = self.DATA / "index"
        self.PROMPT = self.DATA / "prompt"
        self.CONTEXT = self.DATA / "context"

        # Database
        self.DB = self.ROOT / "database"
        
        # Documents
        self.DOC = self.ROOT / "doc"
        self.IDEA_BASE = self.DOC / "idea_base"
        
        # Logs
        self.LOGS = self.ROOT / "logs"
        
        # Templates
        self.TEMPLATES = self.ROOT / "templates"

        # Meta
        self.META = self.ROOT / "meta"
        self.METADATOS = {
            "type": "",
            "date": "",
            "version": "",
            "description": "",
            "linked_to": "",
            "changelog": ""
        }
        self.SUPPORTED_EXTENSIONS = [".yaml", ".yml", ".md", ".json", ".py", ".csv"]
        
        # Codigo Fuente
        self.SRC = self.ROOT / "src"
        self.CORE = self.SRC / "core"
        self.UTIL = self.CORE / "util"
        self.SCRIPT = self.CORE / "script"

        # Templates
        self.TEMPLATES = self.ROOT / "templates"

        # self._ensure_dirs()

    # Crea todas las carpetas del path automaticamente
    def _ensure_dirs(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Path):
                attr.mkdir(parents=True, exist_ok=True)

config = Config()