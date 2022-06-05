# Interface de Cadastro de Clientes

### Cadastro com banco de dados, Cadastro com relatorio PDF.

[![cadastro.png](https://i.postimg.cc/4NvLXChC/cadastro.png)](https://postimg.cc/kB4Fypcw)


# Documentação

 O código começa importando a biblioteca ttk, que é usada para criar uma janela Tkinter.
 A próxima linha importa o módulo customtkinter, que permite recursos mais avançados do que os encontrados na biblioteca ttk padrão.
 Isso inclui a criação de widgets que não estão disponíveis com widgets ttk padrão e o uso de outras bibliotecas, como sqlite3.
 O código então cria uma instância de um widget de tela e define seu tamanho como A4 (letra) x carta (A4).
 Em seguida, ele cria um novo objeto pdfmetrics da classe pdfbase, que contém todas as métricas necessárias para gerar PDFs de programas Python.
 Ele também define duas fontes: uma chamada TTFont que será usada para texto em documentos e outra chamada SimpleDocTemplate que será usada para imagens em páginas.
 Em seguida, ele cria um objeto Image da classe SimpleDocTemplate do ornitorrinco para que ele possa usar essa imagem ao desenhar em uma página posteriormente neste programa.
 Em seguida, ele abre o navegador da Web para que os usuários possam visualizar o relatório gerado on-line depois de executar o programa localmente ou baixá-lo como um arquivo executável (.exe).
 O código tenta produzir um documento PDF.
 O código importa as bibliotecas necessárias e cria uma instância do widget ttk.
 O widget ttk é usado para criar uma janela que pode ser manipulada pelo usuário.
 Ele também cria uma instância da biblioteca customtkinter que permitirá uma interação mais fácil com os widgets.
 O código então cria uma instância de sqlite3, que é usada para armazenar dados em um banco de dados.
 O código começa criando uma classe chamada Func.
 Esta é a função que será executada quando o programa iniciar.
 Possui duas funções: limpa_tela e conecta_bd.
 O primeiro exclui todo o texto de uma entrada, enquanto o segundo se conecta ao banco de dados SQLite3 e cria uma tabela com três colunas (codigo, nome_cliente, telefone).
 A próxima linha cria uma lista chamada listaclientes que contém todas as entradas da tabela clientes.
 Em seguida, ele executa uma instrução INSERT com valores para cada coluna para criar novas linhas nesta lista.
 Depois disso, ele executa outra instrução SELECT que retorna dados sobre cada linha da tabela clientes ordenada pelo nome_cliente ASC.
 Em seguida, ele exclui todas as linhas da listaclientes, exceto aquelas em que codigo é igual a 0 (a primeira linha) para que não haja mais duplicatas e, em seguida, confirma as alterações feitas no banco de dados após conectar novamente usando a função conecta_bd antes de desconectar novamente usando a função desconecta_bd na última etapa antes de finalmente executar função selectlista que imprime todo o seu conteúdo na tela, além de excluí-los posteriormente
 O código é uma classe com três métodos: def limpa_tela() - exclui todo o texto dos campos de entrada do formulário def conecta_bd() - conecta-se ao banco de dados, abre um cursor e executa uma instrução SQL.
 def desconecta_bd() - desconecta do banco de dados, fecha o cursor e salva as alterações.
Carregue mais...
