import socket, json, time
from crypto.aes_encryption import encrypt_message, decrypt_message
from src.config import (
    REPLAY_TOLERANCE_SECONDS,
    CHAT_HOST,
    CHAT_PORT,
    BUFFER_SIZE,
    K_V,
)

def start_chat_server():

    print(f"[*] Iniciando Servidor Chat em {CHAT_HOST}:{CHAT_PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        server.bind((CHAT_HOST, CHAT_PORT))
        server.listen()

        while True:

            conn, addr = server.accept()

            with conn:
                print(f"\n[+] Conexao recebida de {addr}")

                data = conn.recv(BUFFER_SIZE)

                if not data:
                    continue

                request = json.loads(data.decode())
                print(f"[*] Pedido recebido: {request}")

                ticket_v_encrypted = request["ticket_v"]
                authenticator_encrypted = request["authenticator"]

                try:
                    ticket_json = decrypt_message(
                        K_V,
                        ticket_v_encrypted
                    )
                except ValueError:
                    print("[-] Falha ao abrir o Ticket_v.")
                    continue

                ticket = json.loads(ticket_json)

                k_c_v = ticket["k_c_v"]
                id_c_ticket = ticket["id_c"]

                ts_4 = ticket["ts_4"]
                lifetime = ticket["lifetime_4"]

                if time.time() > ts_4 + lifetime:

                    print("Ticket expirado")

                    continue

                try:
                    auth_json = decrypt_message(
                        k_c_v,
                        authenticator_encrypted
                    )
                except ValueError:
                    print("[-] Falha ao abrir o Autenticador.")
                    continue

                auth = json.loads(auth_json)

                id_c_auth = auth["id_c"]
                ts_5 = auth["ts_5"]

                if id_c_ticket != id_c_auth:
                    continue

                if abs(time.time() - ts_5) > REPLAY_TOLERANCE_SECONDS:
                    continue

                if auth["ad_c"] != ticket["ad_c"]:
                    print("[-] Endereço do cliente não confere.")
                    continue

                print(f"[+] Cliente '{id_c_ticket}' autenticado com sucesso via Autenticador!")

                response = {
                    "ts_5": ts_5 + 1
                }

                encrypted = encrypt_message(
                    k_c_v,
                    json.dumps(response)
                )

                conn.sendall(encrypted)
