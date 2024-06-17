import os
import time
from tqdm import tqdm
import pyodbc

class Conexao:
    def __init__(self):
        self.__conn = None

    def conectar(self):
        self.__conn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=***.database.windows.net;'
            'Database=***_producao;'
            'Uid=*****;'
            'Pwd=Hder523*M4@;'
        )

    def desconectar(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None

    def execute(self, sql):
        try:
            if not self.__conn:
                self.conectar()

            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
        except pyodbc.Error as e:
            # Aqui você pode registrar o erro ou lidar com ele de outra forma
            # Tente reconectar uma vez
            self.desconectar()
            self.conectar()
            # Tente executar o SQL novamente
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()

def registrar_sucesso(log_sucesso, mensagem):
    with open(log_sucesso, 'a') as arquivo:
        arquivo.write(f"Sucesso: {mensagem}\n")

def registrar_erro(log_erro, mensagem):
    with open(log_erro, 'a') as arquivo:
        arquivo.write(f"Erro: {mensagem}\n")

def obter_diretorio_trabalho():
    diretorio_trabalho = input("Digite o local de trabalho: ")
    return os.path.abspath(diretorio_trabalho)

def executar_updates(conexao, arquivo_txt, log_sucesso, log_erro, linhas_por_execucao=1, intervalo_entre_execucoes=1):
    diretorio_trabalho = obter_diretorio_trabalho()

    # Define os caminhos completos para os arquivos
    arquivo_txt = os.path.join(diretorio_trabalho, arquivo_txt)
    log_sucesso = os.path.join(diretorio_trabalho, log_sucesso)
    log_erro = os.path.join(diretorio_trabalho, log_erro)

    # Lê o arquivo TXT e divide as instruções SQL
    with open(arquivo_txt, 'r', encoding='utf8') as arquivo:
        instrucoes_sql = arquivo.read().split(';')

    # Remove espaços em branco e linhas vazias
    instrucoes_sql = [sql.strip() for sql in instrucoes_sql if sql.strip()]

    try:
        # Conecta ao banco de dados e executa as instruções SQL em lotes
        total_linhas = len(instrucoes_sql)
        for i in tqdm(range(0, total_linhas, linhas_por_execucao), desc="Executando Updates"):
            lote_sql = instrucoes_sql[i:i+linhas_por_execucao]
            for sql in lote_sql:
                try:
                    conexao.execute(sql)
                    registrar_sucesso(log_sucesso, f"SQL: {sql}")
                except pyodbc.Error as e:
                    registrar_erro(log_erro, f"SQL: {sql} | Erro: {e}")
            time.sleep(intervalo_entre_execucoes)
        print("Comandos executados com sucesso no banco de dados ;)")
    except pyodbc.Error as e:
        registrar_erro(log_erro, f"Erro ao executar updates: {e}")

if __name__ == "__main__":
    conexao_banco = Conexao()
    arquivo_txt = 'comandosql.txt'
    log_sucesso = 'log_sucesso.txt'
    log_erro = 'log_erro.txt'

    executar_updates(conexao_banco, arquivo_txt, log_sucesso, log_erro, linhas_por_execucao=1, intervalo_entre_execucoes=1)
