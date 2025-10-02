# ---
# type: "script"
# date: ""
# version: "0.1.0"
# description: "configuracion base de modulo autonomo "
# ---
# config.py
from pathlib import Path

class Config:
    def __init__(self):
        self.ROOT = Path(__file__).parent

        self.ARCHIVE = self.ROOT / "archive"
        self.BACKUP = self.ARCHIVE / "backup"
        self.HISTORY = self.ARCHIVE / "history"
        
        self.DATA = self.ROOT / "data"
        self.BITACORA = self.DATA / "bitacora"

        self.DB = self.ROOT / "database"
        

        self.DOC = self.ROOT / "doc"
        self.CONTEXT = self.DOC / "context"
        self.PROMPT = self.DOC / "prompt"

        self.LOGS = self.ROOT / "logs"
        
        self.TEMPLATES = self.ROOT / "templates"

        self.META = self.ROOT / "meta"
        
        self.SRC = self.ROOT / "src"

        self.TEMPLATES = self.ROOT / "templates"

        self._ensure_dirs()

    # Crea todas las carpetas del path automaticamente
    def _ensure_dirs(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Path):
                attr.mkdir(parents=True, exist_ok=True)

config = Config()  # <-- instancia única

# class Bitacora:

# bitacora = Bitacora()


