# Kerberos
Trabalho final da disciplina "CIC0201: Segurança Computacional" que tem como objetivo o estudo prático e a implementação do protocolo de autenticação Kerberos.

## Descrição
Foi implementado um simulador de chat, na arquitetura cliente-servidor, que utiliza autenticação pelo protocolo Kerberos, com chaves simétricas.

## Dependências
Python 3 e pacotes listados no arquivo [requirements.txt](./requirements.txt).

## Instruções para a execução:

### Ubuntu
Primeiramente, entre no diretório do projeto.

Recomenda-se criar um ambiente virtual com:
```bash
python3 -m venv venv
source venv/bin/activate
```

Em seguida, instale as dependências com:
```bash
pip install -r requirements.txt
```

Para simular o projeto, são necessárias **4** janelas do terminal abertas na raiz do projeto (todas com o ambiente virtual ativado):

1. Janela do Servidor AS: execute `python main_as.py`.
2. Janela do Servidor TGS: execute `python main_tgs.py`.
3. Janela do Servidor do Chat: execute `python main_chat_server.py`.
4. Janela do Cliente: execute `python main_client.py` e siga as instruções na tela (mais informações abaixo).

É possível logar como um dos usuários cadastrados no [banco simulado](./src/network/as_server.py) do Servidor AS: 
- Usuário: "alice" | Senha: "senha"
- Usuário: "bob" | Senha: "outrasenha"

Ao logar, os logs dos Servidores e do Cliente exibirão o processo de troca e validação de tickets sendo realizado passo a passo.
Após a autenticação mútua, é possível enviar mensagens pelo terminal do cliente, que aparecerão descriptografadas nos logs do Servidor do Chat.

Para encerrar a conexão do usuário atual e liberar o servidor para o próximo, digite "exit" no terminal do cliente. 
O nosso chat só aceita um usuário ativo por vez atualmente, considerando que se trata apenas de uma simulação de um serviço protegido pelo protocolo de autenticação.
