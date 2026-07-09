from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class PublicKeyCrypto:
    @staticmethod
    def generate_keypair():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        public_key = private_key.public_key()

        return private_key, public_key

    @staticmethod
    def sign_message(message: str, private_key: rsa.RSAPrivateKey) -> bytes:
        signature = private_key.sign(
            data = message.encode('utf-8'),
            algorithm=hashes.SHA256(),
            padding=padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            )
        )

        return signature
    
    @staticmethod
    def verify_signature(message: str, signature: bytes, public_key: rsa.RSAPublicKey) -> bool:
        try:
            public_key.verify(
                signature=signature,
                data=message.encode("utf-8"),
                algorithm=hashes.SHA256(),
                padding=padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                )
            )

            return True
        except InvalidSignature:
            return False