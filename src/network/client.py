import socket, json, time
from src.auth.kdf_hash import derive_client_key
from src.crypto.aes_encryption import decrypt_message
from src.config import (
	AS_HOST,
	AS_PORT,
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
                
                #TODO: em sprints futuras, passaremos esses dados para a funcao que fala com o TGS
                return response_data
                
            except ValueError:
                print("\n[-] ERRO: Falha ao decifrar. A senha esta incorreta ou o pacote foi alterado.")

    except ConnectionRefusedError:
        print("[-] ERRO: Nao foi possível conectar ao AS. O servidor está rodando?")

if __name__ == "__main__":
    request_tgt()