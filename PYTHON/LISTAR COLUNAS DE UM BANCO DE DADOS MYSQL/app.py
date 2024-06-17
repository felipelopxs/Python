import mysql.connector

def listar_colunas_todas_tabelas(host, usuario, senha, banco_dados):
    # Conectando ao banco de dados
    conexao = mysql.connector.connect(
        host=host,
        user='root',
        password='12345678Qq!',
        database= 'cervejariapetropolis20230817'
    )

    cursor = conexao.cursor()

    # Obtendo todas as tabelas do banco de dados
    cursor.execute("SHOW TABLES")
    tabelas = [tabela[0] for tabela in cursor.fetchall()]

    # Exibindo as colunas de todas as tabelas
    resultado = ""
    for tabela in tabelas:
        resultado += f"Tabela: {tabela}\n"
        resultado += "Colunas:\n"
        cursor.execute(f"DESCRIBE {tabela}")
        colunas = [coluna[0] for coluna in cursor.fetchall()]
        for coluna in colunas:
            resultado += coluna + "\n"
        resultado += "\n"

    # Fechando a conexão
    cursor.close()
    conexao.close()

    return resultado

def salvar_em_txt(conteudo, arquivo_saida):
    # Salvando o conteúdo em um arquivo de texto
    with open(arquivo_saida, 'w') as arquivo:
        arquivo.write(conteudo)

    print(f"O resultado foi salvo no arquivo: {arquivo_saida}")

# Configurações de conexão ao banco de dados
host = 'localhost'
usuario = 'seu_usuario'
senha = 'sua_senha'
banco_dados = 'seu_banco_de_dados'

# Chamando a função para listar as colunas de todas as tabelas
resultado = listar_colunas_todas_tabelas(host, usuario, senha, banco_dados)

# Caminho do arquivo de saída
arquivo_saida = r'caminho\colunas.txt'

# Chamando a função para salvar o resultado em um arquivo de texto
salvar_em_txt(resultado, arquivo_saida)
