# utils/should_ignore.py

from pathlib import Path

def should_ignore(path: Path, config: dict) -> bool:
    excl = config.get("exclusions", {}).get("folders", [])
    return any(part in excl for part in path.parts)
