import sys, os

# Pega o caminho absoluto da pasta atual (raiz do projeto) e adiciona a pasta 'src' ao sistema.
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from network.client import request_tgt, request_service_ticket

if __name__ == "__main__":
    tgt_data = request_tgt()
    if tgt_data:
        request_service_ticket(tgt_data)