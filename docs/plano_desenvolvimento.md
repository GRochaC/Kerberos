# WhatsChat - Estrutura de Projeto (Versão Kerberos)


## Organização de Diretórios

```
whatchat/
├── whatchat/                    # Pacote principal
│   ├── __init__.py
│   ├── config.py		  # Configurações do projeto (endereços, portas, tolerâncias de tempo)
│   ├── auth/                   # Autenticação, Derivação de Chave e Tickets
│   │   ├── __init__.py
│   │   ├── user_manager.py     # Gerenciamento de usuários do AS (username, hash_senha/chave_K_c)
│   │   ├── ticket_utils.py     # Funções auxiliares para montar/desmontar Tickets e Autenticadores
│   │   └── kdf_hash.py         # Derivação da chave do cliente via Hash 1000x + Salt
│   │
│   ├── network/               # Comunicação de rede via Sockets TCP puros
│   │   ├── __init__.py
│   │   ├── as_server.py       # Servidor de Autenticação (AS) - Porta 5001
│   │   ├── tgs_server.py      # Servidor de Concessão de Ticket (TGS) - Porta 5002
│   │   ├── chat_server.py     # Servidor de Aplicação (Serviço V) - Porta 5003
│   │   ├── client.py          # Cliente do usuário
│   │   └── message_protocol.py # Protocolo para envelopar mensagens em JSON
│   │
│   ├── crypto/               # Criptografia Simétrica Exclusiva
│   │   ├── __init__.py
│   │   └── aes_encryption.py  # Criptografia AES
│   │
│   └── ui/                   # Interface de usuário (console)
│       ├── __init__.py
│       ├── console_ui.py      # Main loop da interface
│       ├── message_display.py # Formatação de mensagens
│       └── input_handler.py   # Leitura de input do usuário
│
├── tests/                     # Testes unitários e de integração
│   ├── __init__.py
│   ├── test_kerberos_flow.py # Testar o fluxo das 6 mensagens
│   └── test_crypto.py        # Testar a KDF e a encriptação AES
│
├── docs/                      # Documentação
│   ├── RELATORIO_TECNICO.pdf  # Relatório técnico (10 páginas max)
│   ├── plano_desenvolvimento.md  # Este arquivo
│   ├── trabalho_antigo.pdf   # Descrição do trabalho do ano passado
│   ├── trabalho.md  # Descrição atual do trabalho
│   └── GUIA_SETUP.md         # Guia de setup e execução
│
├── main_as.py                # Ponto de entrada do Servidor AS
├── main_tgs.py               # Ponto de entrada do Servidor TGS
├── main_chat.py              # Ponto de entrada do Servidor de Chat
├── main_client.py            # Ponto de entrada do Cliente
├── requirements.txt          # Dependências do projeto
└── README.md                 # Descrição geral do projeto

```


## Pipeline de Desenvolvimento

### Fase 1: Logon e Obtenção do TGT (AS)

**Objetivo:** Autenticar o usuário e entregar o Ticket de Concessão de Ticket ($Ticket_{tgs}$) de forma segura.

1. **Servidor AS (`as_server.py` e `user_manager.py`)**
* Inicializa com um "banco" (JSON ou dicionário) contendo `ID_C` (nome do usuário) e a respectiva chave secreta $K_c$ pré-calculada a partir da senha.
* Conhece a chave secreta compartilhada com o TGS ($K_{tgs}$).

2. **KDF do Cliente (`kdf_hash.py`)**
* Ao rodar o cliente, o usuário digita a senha. O cliente aplica um Hash + Salt 1000 vezes para derivar sua chave de sessão permanente ($K_c$). A senha é então apagada da memória.

3. **Passo 1: $C \rightarrow AS$**
* Envia uma mensagem em texto plano: $ID_C || ID_{tgs} || [cite_start]TS_1$.

4. **Passo 2: $AS \rightarrow C$**
* AS gera uma chave de sessão temporária $K_{c,tgs}$.
* AS gera o TGT: $Ticket_{tgs}=E(K_{tgs},[K_{c,tgs}||ID_C||AD_C||ID_{tgs}||TS_2||Lifetime_2])$.
* AS devolve ao cliente o pacote encriptado com $K_c$: $E(K_c,[K_{c,tgs}||ID_{tgs}||TS_2||Lifetime_2||Ticket_{tgs}])$.
* O cliente usa sua chave para abrir a mensagem, guardando a chave de sessão $K_{c,tgs}$ e o $Ticket_{tgs}$.


### Fase 2: Obtenção do Ticket de Serviço (TGS)

**Objetivo:** Usar o TGT para solicitar um ticket específico para o Servidor de Chat.

1. **Servidor TGS (`tgs_server.py`)**
* Conhece a sua chave secreta ($K_{tgs}$) e a chave compartilhada com o Servidor de Chat ($K_v$).

2. **Passo 3: $C \rightarrow TGS$**
* Cliente quer acessar o Chat ($V$). Ele monta um **Autenticador** : $Authenticator_c=E(K_{c,tgs},[ID_C||AD_C||TS_3])$.
* Envia: $ID_v || Ticket_{tgs} || [cite_start]Authenticator_c$.

3. **Passo 4: $TGS \rightarrow C$**
* TGS abre o TGT com $K_{tgs}$, extrai a $K_{c,tgs}$ e usa para validar o Autenticador. Se a data/hora estiver válida, gera a chave de sessão com o chat ($K_{c,v}$).
* TGS gera o ticket do chat: $Ticket_v=E(K_v,[K_{c,v}||ID_C||AD_C||ID_v||TS_4||Lifetime_4])$.
* Devolve ao cliente encriptado com $K_{c,tgs}$: $E(K_{c,tgs},[K_{c,v}||ID_v||TS_4||Ticket_v])$.


### Fase 3: Autenticação Mútua e Chat (Serviço V)

**Objetivo:** Usar o $Ticket_v$ para conectar ao chat, validar a autenticação mútua e iniciar a troca segura de mensagens.

1. **Servidor de Chat (`chat_server.py`)**
* Conhece sua chave secreta $K_v$.

2. **Passo 5: $C \rightarrow V$**
* Cliente gera novo Autenticador para a aplicação de chat: $Authenticator_c=E(K_{c,v},[ID_C||AD_C||TS_5])$.
* Envia: $Ticket_v || [cite_start]Authenticator_c$.

3. **Passo 6: $V \rightarrow C$ (Autenticação Mútua)**
* O Chat abre o $Ticket_v$, extrai $K_{c,v}$ e valida o Autenticador.
* Ele concede acesso e envia de volta ao cliente para provar sua identidade: $E(K_{c,v},[TS_5+1])$.

4. **Troca de Mensagens (O Chat)**
* Todas as mensagens de bate-papo trocadas entre o Cliente e o Chat Server a partir desse ponto são envelopadas e encriptadas usando a chave $K_{c,v}$ (com algoritmo AES).


## Pipeline de Sprints (Ordem de Implementação)

### Sprint 1: Fundações Criptográficas e Servidor AS

* Setup base, bibliotecas e organização de pastas.
* Implementar `kdf_hash.py` (derivação da senha) e `aes_encryption.py` (cifragem/decifragem genérica).
* Implementar `as_server.py` e o Passo 1 e 2 do cliente.

### Sprint 2: O TGS

* Implementar `tgs_server.py`.
* Implementar a lógica do Autenticador (Timestamp).
* Implementar Passo 3 e 4.

### Sprint 3: O Serviço de Chat e Autenticação Mútua

* Implementar `chat_server.py` preparado para receber conexões.
* Implementar Passo 5 e Passo 6 ($TS_5 + 1$).

### Sprint 4: Interface e Chat Protegido

* Criar as UIs simples no console (login, digitação da mensagem).
* Configurar o envio e recebimento contínuo de mensagens pelo cliente no Servidor V, usando criptografia AES com a chave $K_{c,v}$.

### Sprint 5: Documentação e Finalização

* Escrever Relatório Técnico detalhando a arquitetura dos tickets.
* Gravar o vídeo demonstrativo (cada membro pode explicar uma das entidades: AS, TGS, Serviço e Cliente).


## Checklist de Avaliação

* [ ] Protocolo Kerberos implementado **exclusivamente** com chave simétrica (requisito 1).
* [ ] AS implementado separadamente (requisito 2).
* [ ] TGS implementado separadamente (requisito 3).
* [ ] Serviço de Chat implementado (requisito 4).
* [ ] Login do usuário via senha na UI do Cliente (requisito 5).
* [ ] Derivação da chave do cliente ($K_c$) usando KDF baseada na senha e 1000 repetições de Hash  (requisito 6).
* [ ] Emissão dos tickets $Ticket_{tgs}$ e $Ticket_v$ com sucesso (requisito 7).
* [ ] Autenticação Mútua do Serviço retornando o Timestamp + 1 (requisito 8).
* [ ] Fluxo exato dos 6 passos Cliente $\rightarrow$ AS $\rightarrow$ TGS $\rightarrow$ Serviço (requisito 9).
