from src.auth.kdf_hash import derive_client_key

def test_derive_client_key():
    username = "test_user"
    password = "senha123"
    domain = "Whatsapp2.local"

    key = derive_client_key(password=password, username=username, domain=domain)

    assert isinstance(key, bytes)
    assert len(key) == 44           # 32 bytes originais codificados em base64

def test_derive_client_key_unique():
    key_1 = derive_client_key(password="senha123", username="test_user_1", domain="Whatsapp2.local")
    key_2 = derive_client_key(password="senha123", username="test_user_2", domain="Whatsapp2.local")

    assert key_1 != key_2

def test_derive_client_key_different_domain():
    key1 = derive_client_key(password="senha123", username="test_user", domain="dominioA.local")
    key2 = derive_client_key(password="senha123", username="test_user", domain="dominioB.local")
    assert key1 != key2

def test_derive_client_key_different_password():
    key1 = derive_client_key(password="senha123", username="test_user", domain="Whatsapp2.local")
    key2 = derive_client_key(password="senha456", username="test_user", domain="Whatsapp2.local")
    assert key1 != key2