from src.auth.user_manager import UserManager
from src.auth.certificate_handler import CertificateHandler
from src.crypto.public_key_cripto import PublicKeyCrypto
from cryptography.hazmat.primitives import serialization

class LoginInterface:
    def __init__(self, db_path: str = "config/users.db", certs_dir: str = "certs") -> None:
        self.user_manager = UserManager(db_path=db_path)
        self.cert_handler = CertificateHandler(certs_dir=certs_dir)
        self.current_user = None

    def login(self, username: str, password: str) -> bool:
        if not self.user_manager.authenticate(username=username, password_hash=password): return False

        if not self.cert_handler.generate_client_cert(username=username): return False

        self.current_user = username

        return True

    def logout(self) -> None:
        if self.current_user:
            self.current_user = None

        return

    def register(self, username: str, password: str) -> bool:
        try:
            private_key, public_key = PublicKeyCrypto.generate_keypair()

            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode("utf-8")

            if not self.user_manager.register_user(username=username, 
                                                   password_hash=password, 
                                                   public_key=public_key_pem):
                return False

            if not self.cert_handler.generate_client_cert(username=username):
                return False

            return True
        except Exception as e:
            return False

    def get_current_user(self) -> None | str:
        return self.current_user
