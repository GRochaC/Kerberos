from src.crypto.public_key_cripto import PublicKeyCrypto
from cryptography.hazmat.primitives.asymmetric import rsa
import pytest

@pytest.fixture
def keypairs():
    return PublicKeyCrypto.generate_keypair()

def test_generate_keypair():
    pairs = PublicKeyCrypto.generate_keypair()

    assert isinstance(pairs, tuple)
    assert isinstance(pairs[0], rsa.RSAPrivateKey)
    assert isinstance(pairs[1], rsa.RSAPublicKey)

def test_sign_message(keypairs):
    signature = PublicKeyCrypto.sign_message(
        message="test_signature",
        private_key=keypairs[0]
    )

    assert isinstance(signature, bytes)
    assert len(signature) == 256

def test_sign_message_unique(keypairs):
    sig_1 = PublicKeyCrypto.sign_message(
        message="test_same_message",
        private_key=keypairs[0]
    )

    sig_2 = PublicKeyCrypto.sign_message(
        message="test_same_message",
        private_key=keypairs[0]
    )

    assert sig_1 != sig_2

def test_verify_signature_true(keypairs):
    message = "test_message"

    signature = PublicKeyCrypto.sign_message(
        message=message,
        private_key=keypairs[0]
    )

    assert PublicKeyCrypto.verify_signature(
        message=message,
        signature=signature,
        public_key=keypairs[1]
    )

def test_verify_signature_false_1(keypairs):
    message = "test_message"

    signature = PublicKeyCrypto.sign_message(
        message=message,
        private_key=keypairs[0]
    )

    new_message = "test_new_message"

    assert not PublicKeyCrypto.verify_signature(
        message=new_message,
        signature=signature,
        public_key=keypairs[1]
    )

def test_verify_signature_false_2(keypairs):
    message = "test_message"

    signature = PublicKeyCrypto.sign_message(
        message=message,
        private_key=keypairs[0]
    )

    fake_signature = b"fake_signature"

    assert not PublicKeyCrypto.verify_signature(
        message=message,
        signature=fake_signature,
        public_key=keypairs[1]
    )
