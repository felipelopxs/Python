import mysql.connector
import time
from queue import Queue, Empty
from threading import Thread

# Configurações de conexão ao banco de dados
config = {
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'host': 'localhost',  # ou o endereço do seu servidor MySQL
    'database': 'nome_do_banco_de_dados',
    'raise_on_warnings': True
}

# Fila para armazenar os blocos de consultas
fila_consultas = Queue()

# Função para executar a consulta SQL
def executar_consulta(consulta):
    # Conectando ao banco de dados
    conn = mysql.connector.connect(**config)
    
    # Criando um cursor
    cursor = conn.cursor()

    # Executando a consulta
    cursor.execute(consulta)

    # Obtendo os resultados
    resultados = cursor.fetchall()

    # Exibindo os resultados
    for resultado in resultados:
        print(resultado)

    # Fechando o cursor e a conexão
    cursor.close()
    conn.close()

# Função para processar a fila de consultas
def processar_fila():
    while True:
        try:
            consulta = fila_consultas.get(timeout=5)  # Espera por até 5 segundos por uma nova consulta
            print("Executando consulta:")
            executar_consulta(consulta)
            print("Consulta concluída.")
            fila_consultas.task_done()
            time.sleep(60)  # Intervalo de 1 minuto
        except Empty:
            pass

# Iniciando a thread para processar a fila
thread_processamento = Thread(target=processar_fila)
thread_processamento.daemon = True
thread_processamento.start()

# Blocos de consultas para serem executados
blocos_consultas = [
    "SELECT * FROM tabela1",
    "SELECT * FROM tabela2",
    "SELECT * FROM tabela3"
]

# Adicionando os blocos de consultas à fila
for consulta in blocos_consultas:
    fila_consultas.put(consulta)

# Aguardando a conclusão de todas as consultas
fila_consultas.join()

print("Todas as consultas foram concluídas.")
