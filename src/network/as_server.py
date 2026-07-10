import socket, json, time, os, base64
from src.crypto.aes_encryption import encrypt_message
from src.config import (
	REPLAY_TOLERANCE_SECONDS, 
	LIFETIME_TGT_SECONDS,
	AS_HOST,
	AS_PORT,
    BUFFER_SIZE,
)

K_TGS = base64.urlsafe_b64encode(os.urandom(32)) # Chave secreta do TGS (K_tgs), usada tambem pelo AS
USERS_DB = {
    "alice": b"gerar exemplo base 64 com kdf_hash.py" 
}

def start_as_server():
    print(f"[*] Iniciando Servidor de Autenticacao (AS) em {AS_HOST}:{AS_PORT}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((AS_HOST, AS_PORT))
        server_socket.listen()
        
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"\n[+] Conexao recebida de {addr}")
                
                # C -> AS (em texto plano)
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    continue
                
                request = json.loads(data.decode('utf-8'))
                print(f"[*] Pedido recebido: {request}")
                
                id_c = request.get("id_c")
                id_tgs = request.get("id_tgs")
                ts_1 = request.get("ts_1")
                
                ts_cur = time.time()
                if abs(ts_cur - ts_1) > REPLAY_TOLERANCE_SECONDS:
                    print("[-] Timestamp invalido ou muito antigo. Possivel ataque de replay")

                if id_c not in USERS_DB:
                    print("[-] Usuario nao encontrado. Abortando...")
                    continue
                
                k_c = USERS_DB[id_c]
                
                # Chave de sessao (K_c,tgs)
                k_c_tgs_bytes = os.urandom(32)
                k_c_tgs = base64.urlsafe_b64encode(k_c_tgs_bytes).decode('utf-8')
                
                ts_2 = time.time()
                lifetime_2 = LIFETIME_TGT_SECONDS
                ad_c = addr[0]
                
                # Ticket_tgs = E(K_tgs, [K_c,tgs || ID_C || AD_C || ID_tgs || TS_2 || Lifetime_2])
                ticket_tgs_dict = {
                    "k_c_tgs": k_c_tgs,
                    "id_c": id_c,
                    "ad_c": ad_c,
                    "id_tgs": id_tgs,
                    "ts_2": ts_2,
                    "lifetime_2": lifetime_2
                }
                
                ticket_tgs_json = json.dumps(ticket_tgs_dict)
                ticket_tgs_encrypted = encrypt_message(K_TGS, ticket_tgs_json).decode('utf-8')
                
                # Resposta = E(K_c, [K_c,tgs || ID_tgs || TS_2 || Lifetime_2 || Ticket_tgs])
                response_dict = {
                    "k_c_tgs": k_c_tgs,
                    "id_tgs": id_tgs,
                    "ts_2": ts_2,
                    "lifetime_2": lifetime_2,
                    "ticket_tgs": ticket_tgs_encrypted
                }
                
                response_json = json.dumps(response_dict)
                final_encrypted_response = encrypt_message(k_c, response_json)
                conn.sendall(final_encrypted_response)
                print("[*] TGT encriptado e enviado com sucesso!")

if __name__ == "__main__":
    start_as_server()