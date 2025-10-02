import difflib

def generate_diff(original: dict, fixed: dict, file_name: str) -> str:
    """Genera diff legible para humanos"""
    original_str = yaml.dump(original, sort_keys=False)
    fixed_str = yaml.dump(fixed, sort_keys=False)
    
    diff = difflib.unified_diff(
        original_str.splitlines(),
        fixed_str.splitlines(),
        fromfile=f'Original: {file_name}',
        tofile=f'Modificado: {file_name}',
        lineterm=''
    )
    return '\n'.join(diff)