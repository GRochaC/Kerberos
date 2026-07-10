import socket, json, time
from src.auth.kdf_hash import derive_client_key
from src.crypto.aes_encryption import encrypt_message, decrypt_message
from src.config import (
	AS_HOST,
	AS_PORT,
	TGS_HOST,
	TGS_PORT,
    BUFFER_SIZE
)

def request_tgt():
    print("=== Login no WhatsChat (Kerberos) ===")
    id_c = input("Usuario: ").strip()
    password = input("Senha: ").strip()
    
    print("\n[*] Derivando chave K_c localmente...")
    k_c = derive_client_key(password, id_c)
    
    # C -> AS
    id_tgs = "ServidorTGS"
    ts_1 = time.time()
    
    request_data = {
        "id_c": id_c,
        "id_tgs": id_tgs,
        "ts_1": ts_1
    }
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"[*] Conectando ao AS ({AS_HOST}:{AS_PORT})...")
            s.connect((AS_HOST, AS_PORT))
            
            print(f"[*] Enviando Passo 1 (C -> AS): {request_data}")
            s.sendall(json.dumps(request_data).encode('utf-8'))
            
            encrypted_response = s.recv(BUFFER_SIZE)
            if not encrypted_response:
                print("[-] Nenhuma resposta do servidor.")
                return
            
            print("[*] Resposta encriptada recebida do AS. Tentando decifrar...")
            
            try:
                decrypted_json = decrypt_message(k_c, encrypted_response)
                response_data = json.loads(decrypted_json)
                
                print("\n[+] SUCESSO! Senha correta e pacote decifrado.")
                print(f"[*] Chave de Sessao (K_c,tgs): {response_data['k_c_tgs']}")
                print(f"[*] Ticket do TGS (Ticket_tgs): {response_data['ticket_tgs'][:30]}... (oculto)")
                print("\n[+] Você tem um TGT valido!")

                response_data["id_c"] = id_c  # guardado localmente para usar no Passo 3
                return response_data
                
            except ValueError:
                print("\n[-] ERRO: Falha ao decifrar. A senha esta incorreta ou o pacote foi alterado.")
                return None

    except ConnectionRefusedError:
        print("[-] ERRO: Nao foi possível conectar ao AS. O servidor está rodando?")
        return None


def request_service_ticket(tgt_data: dict):
    """
    Passo 3 (C -> TGS) e Passo 4 (TGS -> C).
    Recebe os dados do TGT obtidos em request_tgt() e troca o Ticket_tgs
    por um Ticket_v (ticket de servico para acessar o Chat).
    """
    id_c = tgt_data["id_c"]
    k_c_tgs = tgt_data["k_c_tgs"]
    ticket_tgs = tgt_data["ticket_tgs"]

    id_v = "ServidorChat"
    ts_3 = time.time()

    # Autenticador: prova que o cliente e o dono do ticket, sem reenviar a senha
    ip_do_cliente = socket.gethostbyname(socket.gethostname())
    authenticator_dict = {
        "id_c": id_c,
        "ad_c": ip_do_cliente,
        "ts_3": ts_3,
    }
    authenticator_json = json.dumps(authenticator_dict)
    authenticator_encrypted = encrypt_message(k_c_tgs, authenticator_json).decode('utf-8')

    # Pacote do Passo 3: ID_v || Ticket_tgs || Authenticator_c
    request_data = {
        "id_v": id_v,
        "ticket_tgs": ticket_tgs,
        "authenticator": authenticator_encrypted,
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"[*] Conectando ao TGS ({TGS_HOST}:{TGS_PORT})...")
            s.connect((TGS_HOST, TGS_PORT))

            print(f"[*] Enviando Passo 3 (C -> TGS): id_v={id_v}")
            s.sendall(json.dumps(request_data).encode('utf-8'))

            encrypted_response = s.recv(BUFFER_SIZE)
            if not encrypted_response:
                print("[-] Nenhuma resposta do TGS.")
                return None

            # Passo 4 (TGS -> C): descriptografar com a chave de sessao ANTIGA (K_c,tgs)
            try:
                decrypted_json = decrypt_message(k_c_tgs, encrypted_response)
                response_data = json.loads(decrypted_json)

                print(f"[*] Nova Chave de Sessao (K_c,v): {response_data['k_c_v']}")
                print(f"[*] Ticket de Servico (Ticket_v): {response_data['ticket_v'][:30]}... (oculto)")
                print("\n[+] Ticket de Serviço obtido! Pronto para acessar o Chat.")

                return response_data

            except ValueError:
                print("\n[-] ERRO: Falha ao decifrar a resposta do TGS.")
                return None

    except ConnectionRefusedError:
        print("[-] ERRO: Nao foi possível conectar ao TGS. O servidor está rodando?")
        return None


if __name__ == "__main__":
    tgt_data = request_tgt()
    if tgt_data:
        request_service_ticket(tgt_data)