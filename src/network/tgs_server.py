import socket, json, time, os, base64
from crypto.aes_encryption import encrypt_message, decrypt_message
from config import (
    REPLAY_TOLERANCE_SECONDS,
    LIFETIME_SERVICE_SECONDS,
    TGS_HOST,
    TGS_PORT,
    BUFFER_SIZE,
    K_TGS,
    K_V,
)


def start_tgs_server():
    print(f"[*] Iniciando Servidor de Concessao de Tickets (TGS) em {TGS_HOST}:{TGS_PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((TGS_HOST, TGS_PORT))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"\n[+] Conexao recebida de {addr}")

                # Passo 3 (C -> TGS), em texto plano:
                # { "id_v": ..., "ticket_tgs": ..., "authenticator": ... }
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    continue

                request = json.loads(data.decode('utf-8'))
                print(f"[*] Pedido recebido: {request}")

                id_v = request.get("id_v")
                ticket_tgs_encrypted = request.get("ticket_tgs")
                authenticator_encrypted = request.get("authenticator")

                # 1) Abrir o Ticket_tgs com K_TGS (a mesma chave usada pelo AS)
                try:
                    ticket_tgs_json = decrypt_message(K_TGS, ticket_tgs_encrypted)
                except ValueError:
                    print("[-] Falha ao abrir o Ticket_tgs. Ticket invalido/forjado ou K_TGS nao bate com o AS.")
                    continue

                ticket_tgs = json.loads(ticket_tgs_json)

                # 2) Extrair a chave de sessao (K_c,tgs) e o ID do usuario, de DENTRO do ticket
                k_c_tgs = ticket_tgs["k_c_tgs"]
                id_c_ticket = ticket_tgs["id_c"]
                ad_c_ticket = ticket_tgs["ad_c"]

                # Verifica se o TGT ja expirou
                ts_2 = ticket_tgs["ts_2"]
                lifetime_2 = ticket_tgs["lifetime_2"]
                if time.time() > ts_2 + lifetime_2:
                    print("[-] Ticket_tgs expirado.")
                    continue

                # 3) Abrir o Autenticador usando a K_c,tgs recem-descoberta
                try:
                    authenticator_json = decrypt_message(k_c_tgs, authenticator_encrypted)
                except ValueError:
                    print("[-] Falha ao abrir o Autenticador (chave de sessao incorreta).")
                    continue

                authenticator = json.loads(authenticator_json)

                # 4) Validacoes de seguranca
                id_c_auth = authenticator["id_c"]
                ts_3 = authenticator["ts_3"]

                if id_c_auth != id_c_ticket:
                    print("[-] ID do Autenticador nao bate com o ID do Ticket. Possivel ataque.")
                    continue

                if abs(time.time() - ts_3) > REPLAY_TOLERANCE_SECONDS:
                    print("[-] Timestamp do Autenticador invalido ou muito antigo. Possivel ataque de replay.")
                    continue

                print(f"[+] Cliente '{id_c_ticket}' autenticado com sucesso via Autenticador!")

                # 5) Gerar a nova chave de sessao K_c,v (Cliente <-> Servidor de Chat)
                k_c_v_bytes = os.urandom(32)
                k_c_v = base64.urlsafe_b64encode(k_c_v_bytes).decode('utf-8')

                ts_4 = time.time()
                lifetime_4 = LIFETIME_SERVICE_SECONDS

                # Ticket_v = E(K_v, [K_c,v || ID_C || AD_C || ID_v || TS_4 || Lifetime_4])
                ticket_v_dict = {
                    "k_c_v": k_c_v,
                    "id_c": id_c_ticket,
                    "ad_c": ad_c_ticket,
                    "id_v": id_v,
                    "ts_4": ts_4,
                    "lifetime_4": lifetime_4,
                }
                ticket_v_json = json.dumps(ticket_v_dict)
                ticket_v_encrypted = encrypt_message(K_V, ticket_v_json).decode('utf-8')

                # Resposta = E(K_c,tgs, [K_c,v || ID_v || TS_4 || Ticket_v])
                response_dict = {
                    "k_c_v": k_c_v,
                    "id_v": id_v,
                    "ts_4": ts_4,
                    "ticket_v": ticket_v_encrypted,
                }
                response_json = json.dumps(response_dict)
                final_encrypted_response = encrypt_message(k_c_tgs, response_json)

                conn.sendall(final_encrypted_response)
                print("[*] Ticket de Servico encriptado e enviado com sucesso!")


if __name__ == "__main__":
    start_tgs_server()