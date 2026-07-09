# tests/test_login.py

import pytest
import os
import shutil
from src.auth.login import LoginInterface

@pytest.fixture
def login_clean():
    db_path = "tests/test_login_users.db"
    certs_dir = "tests/test_login_certs"
    
    # Limpar antigos
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(certs_dir):
        shutil.rmtree(certs_dir)
    
    login = LoginInterface(db_path, certs_dir)
    yield login
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(certs_dir):
        shutil.rmtree(certs_dir)

def test_register(login_clean):
    assert login_clean.register("test_user", "senha123") == True
    assert (login_clean.cert_handler.certs_dir / "test_user.crt").exists()
    assert (login_clean.cert_handler.certs_dir / "test_user.key").exists()

def test_register_duplicate(login_clean):
    login_clean.register("test_user", "senha123")
    assert login_clean.register("test_user", "outra") == False

def test_login_true(login_clean):
    login_clean.register("test_user", "senha123")
    assert login_clean.login("test_user", "senha123") == True
    assert login_clean.get_current_user() == "test_user"

def test_login_false(login_clean):
    login_clean.register("test_user", "senha123")
    assert login_clean.login("test_user", "errado") == False
    assert login_clean.get_current_user() is None

def test_login_nonexistent(login_clean):
    assert login_clean.login("test_nonexistent_user", "qualquer") == False
    assert login_clean.get_current_user() is None

def test_logout(login_clean):
    login_clean.register("test_user", "senha123")
    login_clean.login("test_user", "senha123")
    assert login_clean.get_current_user() == "test_user"
    
    login_clean.logout()
    assert login_clean.get_current_user() is None

def test_login_flow(login_clean):
    assert login_clean.register("test_user", "senha123") == True
    
    assert login_clean.login("test_user", "senha123") == True
    assert login_clean.get_current_user() == "test_user"
    
    login_clean.logout()
    assert login_clean.get_current_user() is None
    
    assert login_clean.login("test_user", "senha123") == True
    assert login_clean.get_current_user() == "test_user"