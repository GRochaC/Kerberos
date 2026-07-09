import os, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

NONCE_SIZE = 12

def encrypt_message(key_base64: bytes, plaintext: str) -> bytes:
    """
    Criptografa um  texto com AES-GCM. Retorna o ciphertext em Base64, incluindo o Nonce.
    """
    key = base64.urlsafe_b64decode(key_base64)
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE) # Number used ONCE (aleatorio). Nao e secreto, apenas para inicializar
    plaintext_bytes = plaintext.encode('utf-8')
    
    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, associated_data=None)
    
    return base64.urlsafe_b64encode(nonce + ciphertext)


def decrypt_message(key_base64: bytes, encrypted_payload_base64: bytes) -> str:
    """
    Descriptografa a mensagem. O AES-GCM garante tambem a integridade (erro de InvalidTag).
    """
    key = base64.urlsafe_b64decode(key_base64)
    aesgcm = AESGCM(key)
    
    nonce_ciphertext = base64.urlsafe_b64decode(encrypted_payload_base64)
    nonce = nonce_ciphertext[:NONCE_SIZE]
    ciphertext = nonce_ciphertext[NONCE_SIZE:]
    
    try:
        plaintext_bytes = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
        return plaintext_bytes.decode('utf-8')
    except InvalidTag: raise ValueError("Falha de integridade na mensagem ou chave incorreta")
