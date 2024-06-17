import os
import sys
import pyodbc
import msvcrt
import getpass
import requests
import json as js
import pandas as pd
from tqdm import tqdm
from base64 import b64encode

# Usuário para consulta ao banco de dados
ubd = '******'
pbd = '***@***$17'

def logo():
    print("""
    
█▀█ █▀█ █▀ ▀█▀   █▀▄ █▀▀   █▀▄ █▀█ █▀▀ █░█ █▀▄▀█ █▀▀ █▄░█ ▀█▀ █▀█   ▄▄   ▄▀█ █▀█ █▀█ █▀▀ █▀▀ █▀▄
█▀▀ █▄█ ▄█ ░█░   █▄▀ ██▄   █▄▀ █▄█ █▄▄ █▄█ █░▀░█ ██▄ █░▀█ ░█░ █▄█   ░░   █▀█ █▀▄ ▀▀█ █▄█ ██▄ █▄▀
                
            ░█████╗░██████╗░░██████╗░██╗░░░██╗██╗██╗░░░██╗░█████╗░██████╗░
            ██╔══██╗██╔══██╗██╔═══██╗██║░░░██║██║██║░░░██║██╔══██╗██╔══██╗
            ███████║██████╔╝██║██╗██║██║░░░██║██║╚██╗░██╔╝███████║██████╔╝
            ██╔══██║██╔══██╗╚██████╔╝██║░░░██║██║░╚████╔╝░██╔══██║██╔══██╗
            ██║░░██║██║░░██║░╚═██╔═╝░╚██████╔╝██║░░╚██╔╝░░██║░░██║██║░░██║
            ╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝
            """);

def base64conv(arquivo):

    with open(arquivo, 'rb') as arquivoProcesso:
        base64 = b64encode(arquivoProcesso.read())
        
    base64 = str(base64)
    base64 = base64[2:]
    base64 = base64[:-1]
    
    return base64
    
def coletandoIdArvore(label):
    
    # Configurar a conexão com o banco de dados
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=***.database.windows.net;"  # Nome do servidor SQL Server
        "Database=***_producao;"          # Nome do banco de dados
        "Uid="+ubd+";"                         # Nome de usuário
        "Pwd="+pbd+";"                         # Senha do usuário
    )

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para verificar a existência do nome de arquivo
    cursor.execute("""SELECT DISTINCT Id 
                      FROM GedConfCliente.ArvoreOrganizacional 
                      WHERE LabelArvoreCompleta = ?
                      AND IdCliente = '328E6C72-D83B-4917-***********'""", (label))
    
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    return resultado

def mascara_senha(prompt='Senha: '):
    senha = ''
    print(prompt, end='', flush=True)
    while True:
        ch = msvcrt.getch()
        if ch == b'\r' or ch == b'\n':  # Se o usuário pressionar Enter, encerra o loop
            print()
            break
        elif ch == b'\x08':  # Se o usuário pressionar Backspace, remove o último caractere digitado
            if len(senha) > 0:
                senha = senha[:-1]
                print('\b \b', end='', flush=True)  # Apaga o último asterisco
        else:
            senha += ch.decode('utf-8')
            print('*', end='', flush=True)  # Exibe um asterisco

    return senha

def auth(usuario, senha):

    url_api = "https://integracao.***.com/api/Autenticacao/Login"

    cabecalho = {
        'Content-Type': 'application/json; charset=UTF-8',
        'user-agent': 'RequisicaoWeb'
    }

    corpo = {
        "username": f"{usuario}",
        "password": f"{senha}",
        "tempoExpiracao": 0,
        "utilizacaoUnica": True
    }
    
    response = requests.post(url=url_api, headers=cabecalho, json=corpo)

    if response.status_code == 200 or response.status_code == 201:
        # print(f"Autenticação realizada com sucesso!")
        return response.text
        
    else:
        return response.text
    
def post(dt, idUnidade, idCliente, idArvoreOrganizacional, dados, token, contador):
    url_api = "https://integracao.***.com/api/Documento/Post"

    cabecalho = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json; charset=UTF-8',
        'user-agent': 'RequisicaoWeb'
        }

    parametros = {
        "idUnidade": f"{idUnidade}",
        "idCliente": f"{idCliente}",
        "idArvoreOrganizacional": f"{idArvoreOrganizacional}"
        }
    
    
    chapa = dados["valoresCampos"][0]["valorCampo"]
    
    response = requests.post(url=url_api, params=parametros, headers=cabecalho, json=dados)
    
    if response.status_code == 200 or response.status_code == 201:
        with open ( dt + "\\Log\\00_Log_Sucesso.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"Linha: {contador} | Chapa: {chapa} | IdDocumento: {response.text[50:-2].upper()}\n")
        
    else:
        with open (dt + "\\Log\\00_Log_Erro.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"Linha: {contador} {response.text}\n")

logo()
usuario = input("\nUsuário de cadastro: ")
senha = mascara_senha()
print("\n")

autenticacao = auth(usuario, senha)
autenticacao = js.loads(autenticacao)

token = autenticacao["Token"]

df = pd.read_excel(r"planilha\json2.xlsx")



loop_encerrado = False
ultimo_indice = 0
contador = 2

if os.path.isfile("ultimo_indice.txt"):
    with open("ultimo_indice.txt", "r") as arquivo:
        ultimo_indice = int(arquivo.read())

while not loop_encerrado:

    try:
    
        for index, row in tqdm(df.iterrows(), total=len(df)):
        
            if index < ultimo_indice:
                continue
        
            dt = r"D:\Cebolinha\OneDrive - *** Franchising Ltda\General\TASK\Felipe\PHYTON\POST DOCUMENTO VIA API"
            idUnidade = "f050d53e-3f34-4**************"
            idCliente = "328e6c72-d83b-4**************"
        
            arvoreOrganizacional = row["PR_ArvoreOrganizacional"]
            idArvoreOrganizacional = str(coletandoIdArvore(arvoreOrganizacional))[2:-3].lower()
            #idArvoreOrganizacional = idArvoreOrganizacional[2:-3].lower()
            #imagem = row["CC_Imagem"]
            #caminho = row["Caminho"]
            #cpf = str(row["CL_CPF"])
            #cpf = str(cpf.zfill(11))
            #caminhoImagem = caminho
            json = js.loads(row["Json"])
            #json["arquivos"][0]["arquivo"] = arquivo_base64
            #json["arquivos"][0]["nomeAmigavel"] = imagem
            #json["valoresCampos"][0]["valorCampo"] = cpf
            
            post(dt, idUnidade, idCliente, idArvoreOrganizacional, json, token, contador)
            
            contador += 1
            
            ultimo_indice = index
            
            with open("ultimo_indice.txt", "w") as arquivo:
                arquivo.write(str(ultimo_indice))
                             
            
        loop_encerrado = True
                
    except KeyboardInterrupt:
    
        resposta = input("\nDeseja encerrar o processo? (S/N): ")
        
        if resposta.upper() == "S":
            input("\nPressione Enter para sair...")
            sys.exit()
            
        elif resposta.upper() == "N":
            os.system('cls' if os.name == 'nt' else 'clear')
            logo()
            print(f"Usuário de cadastro: {usuario}")
            print(f"Senha: ***")
            pass

if loop_encerrado:
    input("\nPressione Enter para sair...")
    sys.exit()