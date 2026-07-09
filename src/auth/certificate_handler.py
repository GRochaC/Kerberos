from pathlib import Path
import subprocess

class CertificateHandler:
    def __init__(self, certs_dir = "certs") -> None:
        self.certs_dir = Path(certs_dir)

        self.certs_dir.mkdir(exist_ok=True)

    def generate_ca_cert(self):
        ca_key = self.certs_dir / "ca.key"
        ca_crt = self.certs_dir / "ca.crt"

        if ca_key.exists() and ca_crt.exists: return True

        try:
            subprocess.run([
                "openssl", "genrsa", "-out", str(ca_key), "2048"
            ], check=True, capture_output=True)

            subprocess.run([
                "openssl", "req", "-new", "-x509",
                "-days", "365",
                "-key", str(ca_key),
                "-out", str(ca_crt),
                "-subj", "/C=BR/ST=DF/L=Brasilia/O=UnB/CN=Whatsapp2-CA"
            ], check=True, capture_output=True)

            return True
        except subprocess.CalledProcessError:
            return False

    def generate_client_cert(self, username: str) -> bool:
        if not self.generate_ca_cert():
            return False
        
        ca_key = self.certs_dir / "ca.key"
        ca_crt = self.certs_dir / "ca.crt"
        
        client_key = self.certs_dir / f"{username}.key"
        client_crt = self.certs_dir / f"{username}.crt"
        client_csr = self.certs_dir / f"{username}.csr"
        
        if client_key.exists() and client_crt.exists():
            return True
        
        try:
            subprocess.run([
                "openssl", "genrsa",
                "-out", str(client_key),
                "2048"
            ], check=True, capture_output=True)
            
            subprocess.run([
                "openssl", "req", "-new",
                "-key", str(client_key),
                "-out", str(client_csr),
                "-subj", f"/C=BR/ST=DF/L=Brasilia/O=UnB/CN={username}"
            ], check=True, capture_output=True)

            #Assinar CSR com CA (gera certificado final)
            subprocess.run([
                "openssl", "x509", "-req",
                "-days", "365",
                "-in", str(client_csr),
                "-CA", str(ca_crt),
                "-CAkey", str(ca_key),
                "-CAcreateserial",
                "-out", str(client_crt)
            ], check=True, capture_output=True)
            
            client_csr.unlink()
            
            return True
        except subprocess.CalledProcessError:
            return False

    def cert_exists(self, username: str) -> bool:
        client_key = self.certs_dir / f"{username}.key"
        client_crt = self.certs_dir / f"{username}.crt"
        
        return client_key.exists() and client_crt.exists()