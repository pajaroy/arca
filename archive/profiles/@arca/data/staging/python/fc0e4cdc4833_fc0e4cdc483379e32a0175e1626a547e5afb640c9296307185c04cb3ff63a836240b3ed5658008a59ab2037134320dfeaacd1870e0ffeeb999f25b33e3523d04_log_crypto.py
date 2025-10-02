from cryptography.fernet import Fernet
import os
import base64
import logging

# Key management
KEY_PATH = os.getenv("LOG_CRYPTO_KEY_PATH", ".logkey")
ENCRYPTION_ENABLED = os.getenv("LOG_ENCRYPTION_ENABLED", "false").lower() == "true"

def _get_key():
    """Generate or load encryption key"""
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as key_file:
            return key_file.read()
    
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)
    return key

def encrypt_log(content: str) -> str:
    """Encrypt single log entry"""
    if not ENCRYPTION_ENABLED:
        return content
    
    try:
        f = Fernet(_get_key())
        encrypted = f.encrypt(content.encode())
        return f"ENCRYPTED:{base64.b64encode(encrypted).decode()}"
    except Exception as e:
        logging.error(f"Log encryption failed: {str(e)}")
        return content

def encrypt_file(source_path, dest_path):
    """Encrypt entire log file"""
    try:
        f = Fernet(_get_key())
        with open(source_path, 'rb') as f_in:
            encrypted = f.encrypt(f_in.read())
        with open(dest_path, 'wb') as f_out:
            f_out.write(encrypted)
    except Exception as e:
        logging.error(f"File encryption failed: {str(e)}")

def decrypt_file(source_path, dest_path):
    """Decrypt file for audit purposes"""
    try:
        f = Fernet(_get_key())
        with open(source_path, 'rb') as f_in:
            decrypted = f.decrypt(f_in.read())
        with open(dest_path, 'wb') as f_out:
            f_out.write(decrypted)
    except Exception as e:
        logging.error(f"Decryption failed: {str(e)}")

# CLI decryption example
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--decrypt", nargs=2, metavar=("INPUT", "OUTPUT"))
    args = parser.parse_args()
    
    if args.decrypt:
        decrypt_file(args.decrypt[0], args.decrypt[1])