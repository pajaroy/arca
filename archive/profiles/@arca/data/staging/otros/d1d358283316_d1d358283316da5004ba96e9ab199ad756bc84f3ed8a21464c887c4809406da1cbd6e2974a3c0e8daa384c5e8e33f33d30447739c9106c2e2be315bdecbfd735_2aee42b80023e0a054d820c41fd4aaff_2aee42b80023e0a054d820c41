def log_to_bitacora(entry: dict):
    """Formato markdown para bitácora"""
    with open("bitacora.md", "a") as f:
        f.write(f"\n## {datetime.now().isoformat()}\n")
        f.write(f"- Archivo: {entry['file']}\n")
        f.write(f"- Cambios: {entry['changes']}\n")

def log_to_changelog(entry: dict):
    """Formato YAML estructurado"""
    changelog = {
        "timestamp": datetime.now().isoformat(),
        "file": str(entry['file']),
        "changes": entry['changes']
    }
    # Append a changelog.yaml