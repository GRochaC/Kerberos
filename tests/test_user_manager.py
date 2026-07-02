from src.auth.user_manager import UserManager
import sqlite3
import logging
import pytest
import os
from .conftest import TEST_DB_PATH

@pytest.fixture
def manager():
    if os.path.exists(TEST_DB_PATH): os.remove(TEST_DB_PATH)

    mgr = UserManager(TEST_DB_PATH)

    yield mgr

    if os.path.exists(TEST_DB_PATH): os.remove(TEST_DB_PATH)

def test_init():
    manager = UserManager(TEST_DB_PATH)
    
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table' AND name='users'
        """
    )
    result = cursor.fetchone()
    conn.close()
    
    assert result, "Tabela 'users' não existe."

def test_register_user_true(manager):
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.cursor().execute(
        """
        DELETE FROM users WHERE username='teste_register'
        """
    )

    conn.commit()
    conn.close()

    ret = manager.register_user("teste_register","123","123")

    assert ret, "Usuário já cadastrado."

    conn = sqlite3.connect(TEST_DB_PATH)
    result = conn.cursor().execute(
        """
        SELECT * FROM users WHERE username=?
        """, 
        ("teste_register",)
    ).fetchone()

    conn.close()

    assert result, "Usuário não registrado."

def test_register_user_false(manager):
    manager.register_user("teste_register","321","321")
    ret = manager.register_user("teste_register","123","123")
    assert not ret, "Usuário novo"

def test_authenticate_true(manager):
    manager.register_user("teste_auth","hash_correto","123")
    assert manager.authenticate("teste_auth", "hash_correto"), "Hashes diferentes."

def test_authenticate_false(manager):
    manager.register_user("teste_auth_2","hash_correto","123")
    assert not manager.authenticate("teste_auth_2", "hash_incorreto"), "Hashes iguais."

def test_delete_user_true(manager):
    manager.register_user("teste_delete","123","123")

    ret = manager.delete_user("teste_delete")
    assert ret, "Usuário não deletado."

def test_delete_false(manager):
    ret = manager.delete_user("teste_delete_inexistente")
    assert not ret, "Usário existente."

def test_get_all_users(manager):
    manager.register_user("teste_get_1","123","123")
    manager.register_user("teste_get_2","123","123")
    manager.register_user("teste_get_3","123","123")
    manager.register_user("teste_get_1","123","123")


    ret = manager.get_all_users()

    assert isinstance(ret, list)
    assert len(ret) == 3

def test_get_all_users_empty(manager):
    ret = manager.get_all_users()

    assert ret == []




