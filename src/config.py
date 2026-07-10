# Rede
AS_HOST = '127.0.0.1'
AS_PORT = 5001
TGS_HOST = '127.0.0.1'
TGS_PORT = 5002
CHAT_HOST = '127.0.0.1'
CHAT_PORT = 5003
BUFFER_SIZE = 4096 # tamanho pra recebimento de pacotes

# Tempo / Seguranca
REPLAY_TOLERANCE_SECONDS = 300 # 5 minutos
LIFETIME_TGT_SECONDS = 3600 # 1 hora
LIFETIME_SERVICE_SECONDS = 3600 # 1 hora

# Criptografia
NONCE_SIZE = 12
KDF_ITERATIONS = 1000
SALT_DOMAIN = "kerberos"

# Chaves compartilhadas de longo prazo entre servicos (simulando um keytab).
# IMPORTANTE: sao constantes fixas, e NAO geradas com os.urandom() em runtime,
# porque AS e TGS rodam em processos Python separados. Se cada um gerasse a
# sua propria chave aleatoria ao importar o modulo, as chaves nunca bateriam
# e o TGS nunca conseguiria abrir o Ticket_tgs criado pelo AS.
K_TGS = b'0ELkTn7DvU5Rapwz33pd_Duk5UMQVqouMI5RkA0-ozA='  # Chave compartilhada entre AS e TGS
K_V   = b'lAlpnEtUTxDgTDebmloBYAehGtBQCetmig8MoUesLsQ='  # Chave compartilhada entre TGS e Servidor de Chat