import pytest
from src.auth.certificate_handler import CertificateHandler
import os

@pytest.fixture
def handler():
    certs_dir = "tests/test_certs"
    h = CertificateHandler(certs_dir)
    yield h
    
    # Cleanup
    import shutil
    if os.path.exists(certs_dir):
        shutil.rmtree(certs_dir)

def test_generate_ca_cert(handler):
    assert handler.generate_ca_cert() == True
    assert (handler.certs_dir / "ca.key").exists()
    assert (handler.certs_dir / "ca.crt").exists()

def test_generate_client_cert(handler):
    assert handler.generate_client_cert("test_user") == True
    assert (handler.certs_dir / "test_user.key").exists()
    assert (handler.certs_dir / "test_user.crt").exists()

def test_cert_exists(handler):
    assert handler.cert_exists("test_user") == False
    handler.generate_client_cert("test_user")
    assert handler.cert_exists("test_user") == True

def test_generate_multiple_clients(handler):
    handler.generate_client_cert("test_user")
    handler.generate_client_cert("test_user_2")
    handler.generate_client_cert("test_user_3")
    
    assert handler.cert_exists("test_user")
    assert handler.cert_exists("test_user_2")
    assert handler.cert_exists("test_user_3")