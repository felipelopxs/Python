import pandas as pd
from sqlalchemy import create_engine
import pyodbc

# SUPERCLASSE DE CONEXÃO COM O BANCO DE DADOS
class Conexao:
    def __init__(self) -> None:
        self.__conn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=***.database.windows.net;'
            'Database=***_producao;'
            'Uid=*********;'
            'Pwd=Mig@***$17;'
        )

# Instancie a classe de conexão
conexao = Conexao()

# Criar uma engine do SQLAlchemy usando a conexão existente
engine = create_engine("mssql+pyodbc://", creator=lambda: conexao._Conexao__conn)

# Consulta SQL com LIMIT para limitar o número de linhas
sql_query = "SELECT ..."

# Executar a consulta e obter os resultados como um DataFrame
chunk_size = 100  # Escolha um tamanho de chunk que funcione bem para sua quantidade de dados
df_chunks = pd.read_sql_query(sql_query, engine, chunksize=chunk_size)

# Caminho onde deseja salvar o arquivo XLSX
excel_file_path = r'D:\OneDrive - *** Franchising Ltda\General\TASK\Felipe\***\CAMINHO\metadados.xlsx'

# Adicionar extensão .xlsx ao caminho, se não fornecido
if not excel_file_path.lower().endswith('.xlsx'):
    excel_file_path += '.xlsx'

with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
    for i, chunk in enumerate(df_chunks):
        chunk.to_excel(writer, sheet_name=f'Sheet_{i+1}', index=False)

print(f'Dados salvos em {excel_file_path}')

# Feche a conexão
conexao._Conexao__conn.close()
