## Descrição do Trabalho
O presente trabalho tem como objetivo o estudo prático e a implementação do protocolo de autenticação Kerberos, conforme apresentado em sala de aula e descrito na Aula 10, slides 22, 23 e 24, que se encontram na Semana 10 do Aprender3. A proposta é que os alunos explorem, na prática, os conceitos de autenticação baseada em chaves simétricas, tickets de autenticação, autenticação mútua e gerenciamento de chaves de sessão.


O trabalho deve ser realizado em grupos de até 4 pessoas e entregue até o dia 10/07 na plataforma Aprender3. Vocês deverão entregar os seguintes itens:

- Código completo da aplicação (3,5 pontos);.
- Instruções claras para compilação e execução do programa (0,5 ponto);.
- Relatório técnico (máximo de 10 páginas) (3 pontos), contendo:.
	- Descrição completa da arquitetura desenvolvida;.
	- Descrição detalhada da implementação do Servidor de Autenticação (Authentication Server – AS);.
	- Descrição detalhada da implementação do Servidor de Emissão de Tickets (Ticket Granting Server – TGS);.
	- Explicação detalhada do mecanismo utilizado para derivação de chaves a partir da senha do usuário, incluindo a Função de Derivação de Chave (KDF) adotada;.
	- Explicação detalhada do processo de obtenção e utilização dos tickets de autenticação;.
	- Explicação detalhada do mecanismo de autenticação mútua implementado;.
	- Descrição dos algoritmos criptográficos utilizados e justificativa de sua escolha;.
	- Relato das principais dificuldades encontradas e dos aprendizados obtidos..
- Vídeo de apresentação (3 pontos), com todos os integrantes do grupo participando, cada um apresentando pelo menos uma parte do trabalho e demonstrando domínio sobre a implementação realizada.

## Requisitos mínimos da implementação
A solução desenvolvida deverá obrigatoriamente:

1. Implementar o protocolo Kerberos utilizando exclusivamente criptografia de chave simétrica;.
2. Implementar um Servidor de Autenticação (Authentication Server – AS);.
3. Implementar um Ticket Granting Server (TGS);.
4. Implementar pelo menos um serviço protegido por Kerberos. Exemplos incluem:.
	- Chat cliente-servidor;.
	- Sistema de compartilhamento de arquivos;.
	- API protegida;.
	- Sistema de notas ou qualquer outro serviço similar..
5. Permitir que o usuário realize autenticação por meio de uma senha;.
6. Derivar a chave utilizada pelo cliente a partir da senha utilizando uma Função de Derivação de Chave (KDF);.
7. Implementar a emissão, distribuição e validação de tickets;.
8. Implementar autenticação mútua entre cliente e serviço;.
9. Seguir o fluxo de autenticação apresentado em sala de aula, contemplando as etapas realizadas entre Cliente, AS, TGS e Serviço..

## Restrições
Não é permitido utilizar implementações prontas do protocolo Kerberos ou bibliotecas que automatizem seu funcionamento. O protocolo deverá ser implementado pelos alunos utilizando apenas primitivas criptográficas básicas, tais como algoritmos de criptografia simétrica, funções hash, funções de derivação de chaves (KDFs) e geradores de números aleatórios.

O uso de ferramentas de Inteligência Artificial (IA) para a geração de código ou de partes do relatório não é permitido, a menos que o aluno compreenda plenamente e seja capaz de explicar detalhadamente cada trecho do conteúdo produzido. Qualquer indício de uso indevido de IA, cópia de código pronto ou plágio resultará em penalização na nota final.

## Entrega
Não serão aceitos links para repositórios públicos (com exceção do link para o vídeo de apresentação). Todos os arquivos deverão ser entregues até a data estipulada na plataforma Aprender3.

O relatório deve refletir o entendimento dos alunos, apresentando um texto bem escrito, bem formatado e tecnicamente consistente.

## Observação
O foco principal deste trabalho é a implementação do protocolo Kerberos. A complexidade do serviço protegido é secundária e não será utilizada como principal critério de avaliação. Isso significa que o serviço não precisa estar totalmente funcional; basta que a autenticação do usuário esteja implementada. As demais partes do serviço podem permanecer incompletas. Serão valorizadas implementações corretas do protocolo, clareza arquitetural, qualidade do código, segurança da solução desenvolvida e compreensão dos mecanismos de autenticação envolvidos.