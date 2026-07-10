import sys, os

# Pega o caminho absoluto da pasta atual (raiz do projeto) e adiciona a pasta 'src' ao sistema.
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from network.chat_server import start_chat_server

if __name__ == "__main__":
    start_chat_server()