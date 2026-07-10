import sys, os

# Pega o caminho absoluto da pasta atual (raiz do projeto) e adiciona a pasta 'src' ao sistema.
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from network.tgs_server import start_tgs_server

if __name__ == "__main__":
    start_tgs_server()