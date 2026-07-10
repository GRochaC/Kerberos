import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from src.config import KDF_ITERATIONS, SALT_DOMAIN

def derive_client_key(password: str, username: str, domain: str = SALT_DOMAIN) -> bytes:
    """
    Deriva uma chave simetrica segura a partir da senha do usuário (slide 16 e 17)
    """
    salt_string = f"{domain}{username}"
    salt_bytes = salt_string.encode('utf-8')
    password_bytes = password.encode('utf-8')
    
    # KDF com SHA-256 como hash base
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=KDF_ITERATIONS,
    )
    
    derived_key = kdf.derive(password_bytes)
    return base64.urlsafe_b64encode(derived_key)
