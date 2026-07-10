import pytest
from src.auth.kdf_hash import derive_client_key
from src.crypto.aes_encryption import encrypt_message, decrypt_message

@pytest.fixture
def key():
    return derive_client_key(password="senha123", username="test_user", domain="Whatsapp2.local")

def test_encrypt_decrypt_roundtrip(key):
    msg = "Hello, world!"

    encrypted_msg = encrypt_message(key, msg)

    assert isinstance(encrypted_msg, bytes)

    decrypt_msg = decrypt_message(key, encrypted_msg)

    assert isinstance(decrypt_msg, str)
    assert msg == decrypt_msg

def test_encrypt_decrypt_different_key(key):
    msg = "Hello, world!"

    encrypt_msg = encrypt_message(key, msg)

    wrong_key = derive_client_key(password="senha123", username="test_other_user", domain="Whatsapp2.local")

    with pytest.raises(ValueError):
        decrypt_message(wrong_key, encrypt_msg)


def test_encrypt_unique(key):
    msg = "Hello, world!"

    encrypt_msg_1 = encrypt_message(key, msg)
    encrypt_msg_2 = encrypt_message(key, msg)

    assert encrypt_msg_1 != encrypt_msg_2

def test_decrypt_integrity(key):
    msg = "Hello, world!"

    encrypt_msg  = bytearray(encrypt_message(key, msg))
    encrypt_msg[0] ^= 0xFF

    with pytest.raises(ValueError):
        decrypt_message(key, bytes(encrypt_msg))
