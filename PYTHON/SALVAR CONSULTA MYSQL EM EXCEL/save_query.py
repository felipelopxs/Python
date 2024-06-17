import pandas as pd
import mysql.connector

# Configurações de conexão com o banco de dados MySQL
db_config = {
    'user': 'root',
    'password': '12345678Qq!',
    'host': '127.0.0.1',
    'database': '******olis20230710',
}
# Consulta SQL
query = """
select *****;
"""


# Função para salvar consulta em uma planilha do Excel
def salvar_consulta_excel(query, filename):
    # Conecta ao banco de dados MySQL
    conn = mysql.connector.connect(**db_config)
    
    # Executa a consulta
    cursor = conn.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    
    # Obter nomes das colunas
    column_names = [desc[0] for desc in cursor.description]
    
    # Criar um DataFrame pandas com os resultados da consulta
    df = pd.DataFrame(resultado, columns=column_names)
    
    # Salvar DataFrame em um arquivo Excel
    df.to_excel(filename, index=False)
    
    # Fechar conexão com o banco de dados
    cursor.close()
    conn.close()
    
    print(f"Consulta salva com sucesso no arquivo {filename}")

# Chamar a função para salvar a consulta em uma planilha Excel
salvar_consulta_excel(query, r'Caminho\historico_contrato.xlsx')