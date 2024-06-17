from azure.storage.blob import BlobServiceClient, BlobClient, FileClient
import os
import pyodbc
import fitz
import uuid
from tqdm import tqdm
import time
from urllib.parse import quote
import re



# Variáveis Globais
ubd = '***'   # Usurário Para Acesso ao Banco
pbd = '***' # Senha do Usuário
novo_id_extensao = 1

# Funções
def origem():
    tp = input('\nOS ARQUIVOS QUE DESEJA REALIZAR A ASSOCIAÇÃO SÃO DE ORIGEM [0] LOCAL OU [1] AZURE OU O PROCESSO QUE DESEJA REALIZAR É [2] BACKUP? ')
    
    while tp != '0' and tp != '1' and tp != '2':
        print('\nOPÇÃO INVÁLIDA. POR FAVOR, DIGITE 0 OU 1.')
        tp = input('\nOS ARQUIVOS QUE DESEJA REALIZAR A ASSOCIAÇÃO SÃO DE ORIGEM [0] LOCAL OU [1] AZURE OU O PROCESSO QUE DESEJA REALIZAR É [2] BACKUP? ')
    
    return int(tp)

def contar_paginas_pdf(caminho_arquivo):
    try:
        pdf_doc = fitz.open(caminho_arquivo)
        num_paginas = pdf_doc.page_count
        pdf_doc.close()
        return num_paginas
    except fitz.PDFError:
        # Arquivo não é um PDF válido
        return None
    except Exception as e:
        # Outros erros
        print(f'Erro ao contar páginas do arquivo PDF: {e}')
        return None

def verificar_arquivo(codigo,nome_arquivo):
    '''
    Função para verificar a existência de um nome de arquivo na tabela
    GedDocumento.Imagem para o código de registro.
    '''
    # Configurar a conexão com o banco de dados
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=***.database.windows.net;'  # Nome do servidor SQL Server
        'Database=***_producao;'          # Nome do banco de dados
        'Uid='+ubd+';'                         # Nome de usuário
        'Pwd='+pbd+';'                         # Senha do usuário
    )

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para verificar a existência do nome de arquivo
    cursor.execute('SELECT COUNT(i.Id) FROM GedDocumento.Documento d INNER JOIN GedDocumento.Imagem i ON i.IdDocumento = d.Id AND i._del IS NULL AND d.codigo = ? AND i.Nome = ?', (codigo, nome_arquivo))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Verificar se o nome de arquivo existe
    if resultado[0] > 0:
        return True
    else:
        return False
        
def verificar_usuario(usuario):
    '''
    Função para verificar a existência de um nome de arquivo na tabela
    GedDocumento.Imagem para o código de registro.
    '''
    # Configurar a conexão com o banco de dados
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=***.database.windows.net;'  # Nome do servidor SQL Server
        'Database=***_producao;'          # Nome do banco de dados
        'Uid='+ubd+';'                         # Nome de usuário
        'Pwd='+pbd+';'                         # Senha do usuário
    )

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para verificar a existência do usuario
    cursor.execute('SELECT COUNT(Id) FROM GedSeguranca.Usuario WHERE Id = ?', (usuario))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Verificar se o nome de arquivo existe
    if resultado[0] > 0:
        return True
    else:
        return False
        
def verifica_ext(extensao):
    '''
    Função para verificar a existência da extensão do arquivo
    '''
    # Configurar a conexão com o banco de dados
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=***.database.windows.net;'  # Nome do servidor SQL Server
        'Database=***_producao;'          # Nome do banco de dados
        'Uid='+ubd+';'                         # Nome de usuário
        'Pwd='+pbd+';'                         # Senha do usuário
    )

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para verificar a existência do nome de arquivo
    cursor.execute('SELECT TOP 1 e.Id FROM GedSistema.Extensao e WHERE e.Extensao = ? ORDER BY e.Id', (extensao))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Verificar se o nome de arquivo existe
    return resultado
        
def verificar_pasta(caminho):
    if not os.path.exists(caminho + '\Files'):
        os.makedirs(caminho + '\Files')
        
    if not os.path.exists(caminho + '\Log'):
        os.makedirs(caminho + '\Log')
        
    ptf = caminho + '\Files'
    ptl = caminho + '\Log'
    
    return ptf, ptl
    
def new_id():
    # Gerar um novo Id
    return str(uuid.uuid4())
    
def buscar_documento(codigo):
    '''
    Função para verificar a existência da extensão do arquivo
    '''
    # Configurar a conexão com o banco de dados
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=***.database.windows.net;'  # Nome do servidor SQL Server
        'Database=***_producao;'          # Nome do banco de dados
        'Uid='+ubd+';'                         # Nome de usuário
        'Pwd='+pbd+';'                         # Senha do usuário
    )

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para verificar a existência do nome de arquivo
    cursor.execute('SELECT d.Id FROM GedDocumento.Documento d WHERE d.Codigo = ?', (codigo))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Verificar se o nome de arquivo existe
    return resultado
    
def buscar_dados_uc(iduc):
    '''
    Função para buscar dados da unidade e do cliente
    '''
    # Configurar a conexão com o banco de dados
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=***.database.windows.net;'  # Nome do servidor SQL Server
        'Database=***_producao;'          # Nome do banco de dados
        'Uid='+ubd+';'                         # Nome de usuário
        'Pwd='+pbd+';'                         # Senha do usuário
    )

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para verificar a existência do nome de arquivo
    cursor.execute("SELECT u.Id AS 'IdUnidade', u.Azure_NomeConta, u.Azure_ChaveAcessoPrimario, c.Id AS 'IdCliente' FROM GedHierarquia.UnidadeCliente uc INNER JOIN GedHierarquia.Unidade u ON u.Id = uc.IdUnidade AND uc.Id = ? INNER JOIN GedHierarquia.Cliente c ON c.Id = uc.IdCliente", (iduc))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Verificar se o nome de arquivo existe
    return resultado
    
def buscar_nome_por_id(id):
    '''
    Função para buscar nome do arquivo pelo idimagem
    '''
    # Configurar a conexão com o banco de dados
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=***.database.windows.net;'  # Nome do servidor SQL Server
        'Database=***_producao;'          # Nome do banco de dados
        'Uid='+ubd+';'                         # Nome de usuário
        'Pwd='+pbd+';'                         # Senha do usuário
    )

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para verificar a existência do nome de arquivo
    cursor.execute('SELECT i.Nome FROM GedDocumento.Imagem i WHERE i.Id = ?', (id))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Retornar nome do arquivo
    return resultado
    
def buscar_dados_imagem(id):
    '''
    Função para buscar dados da imagem
    '''
    # Configurar a conexão com o banco de dados
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=***.database.windows.net;'  # Nome do servidor SQL Server
        'Database=***_producao;'          # Nome do banco de dados
        'Uid='+ubd+';'                         # Nome de usuário
        'Pwd='+pbd+';'                         # Senha do usuário
    )

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
 
    # Executar a consulta SQL para verificar a existência do nome de arquivo
    cursor.execute('SELECT i.IdStatusOCR, i.Nome, i.QtdePagina, i.Tamanho, i.IdExtensao, e.Extensao FROM GedDocumento.Imagem i INNER JOIN GedSistema.Extensao e ON e.Id = i.IdExtensao WHERE i.Id = ?', (id))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Retornar nome do arquivo
    return resultado
    
def tratar_url(url):
    url_tratada = quote(url, safe="/:")
    return url_tratada
    
def verifica_id_ext():
    '''
    Função para verificar a existência da extensão do arquivo
    '''
    # Configurar a conexão com o banco de dados
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=***.database.windows.net;'  # Nome do servidor SQL Server
        'Database=***_producao;'          # Nome do banco de dados
        'Uid='+ubd+';'                         # Nome de usuário
        'Pwd='+pbd+';'                         # Senha do usuário
    )

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para verificar a existência do nome de arquivo
    cursor.execute('SELECT MAX(Id) FROM GedSistema.Extensao')
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Verificar se o nome de arquivo existe
    return resultado
    
def tratar_caract(nome):
    nome.replace("\\", " ").replace("/", " ").replace("|", " ").replace("<", " ").replace(">", " ").replace("*", " ").replace(":", " ").replace('"', " ").replace("'", " ").replace("?", " ")
    
    return nome
    
def insert_extensao(comando):
    '''
    Função para verificar a existência da extensão do arquivo
    '''
    # Configurar a conexão com o banco de dados
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=***.database.windows.net;'  # Nome do servidor SQL Server
        'Database=***_producao;'          # Nome do banco de dados
        'Uid='+ubd+';'                         # Nome de usuário
        'Pwd='+pbd+';'                         # Senha do usuário
    )

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para verificar a existência do nome de arquivo
    cursor.execute(f'{comando}')
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

# Aplicação
tp = origem()

if tp == 0:
    pt = input('\nDIGITE O CAMINHO PARA A PASTA DE TRABALHO: ')
    ptf, ptl = verificar_pasta(pt)
    
    user_resp = input('\nDIGITE O IDUSUARIO RESPONSÁVEL PELA ASSOCIAÇÃO: ')
    
    while verificar_usuario(user_resp) == False:
        print('\nIDUSUARIO INVÁLIDO!')
        user_resp = input('\nDIGITE O IDUSUARIO RESPONSÁVEL PELA ASSOCIAÇÃO: ')
    
    uc = input('\nDIGITE O IDUNIDADECLIENTE DE DESTINO DOS ARQUIVOS: ')
    
    while buscar_dados_uc(uc) is None:
        print('\nIDUNIDADECLIENTE INVÁLIDO!')
        uc = input('\nDIGITE O IDUNIDADECLIENTE DE DESTINO DOS ARQUIVOS: ') 
        
    uid, uconta, usenha, cid = buscar_dados_uc(uc)

    # Ler o arquivo TXT
    with open(pt + '\lista-img.txt', 'r') as arquivo:

        # Conta o número total de linhas no arquivo
        total_linhas = sum(1 for linha in arquivo)

        # Reinicia o cursor do arquivo para o início
        arquivo.seek(0)
        
        print('\n')
        for linha in tqdm(arquivo, total=total_linhas, desc='Progresso'):
        
            # Extrair as informações de código, nome de arquivo e caminho
            codigo, nome_arquivo = linha.strip().split('|')
            nome_arquivo = nome_arquivo.replace("'", " ")
            
            # Caminho arquivos
            caminho = pt + "\\Files\\" + nome_arquivo
            
            # Buscando IdDocumento
            iddocumento = str(buscar_documento(codigo)[0])
            
            # Gerando Id para o arquivo
            id = str(new_id())
            
            try:

                # Buscando tamanho do arquivo em bytes
                tamanho = os.path.getsize(caminho)

            except Exception as erro_tamanho:
                with open (ptl + '\\LogErroExistente.txt', 'a') as arquivo:
                    arquivo.write(f"Arquivo '{nome_arquivo}' não existe para obter tamanho'\n")
                continue
            
            # Obtém a extensão do arquivo
            extensao = os.path.splitext(caminho)[1]
            extensao = extensao.replace(".", "").lower()
            
            padrao = re.compile(re.escape(f".{extensao}"), re.IGNORECASE)
            nome_arquivo = padrao.sub("", nome_arquivo)
            nome_arquivo = tratar_caract(nome_arquivo)
    
            # Chamar a função para verificar a existência da extensão do arquivo
            existe_arquivo = verificar_arquivo(codigo, nome_arquivo)
            idextensao = verifica_ext(extensao)
    
            # Exibir o resultado
            if existe_arquivo:
                with open (ptl + '\\arquivo_ja_existentes.txt', 'a') as arquivo:
                    arquivo.write(f'O documento "{codigo}", já possui um arquivo com o nome "{nome_arquivo}" associado.\n')
                
            else:
                if idextensao is not None:
                    num_paginas = contar_paginas_pdf(caminho)
                    if num_paginas is not None:
                        with open(pt + '\\01_ComandoSQL.sql', 'a') as arquivo:
                            arquivo.write(f"INSERT INTO GedDocumento.Imagem VALUES ('{id.upper()}','{iddocumento.upper()}',1,'http://{uconta}.blob.core.windows.net/{cid.lower()}/{id.lower()}.{extensao.lower()}','{nome_arquivo}',{num_paginas},{tamanho},GETDATE(),{idextensao[0]},'{user_resp.upper()}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);\n")
                         
                        with open(ptl + '\\logSucessoInsert.txt', 'a') as arquivo:
                           arquivo.write(f"DE: {nome_arquivo} | PARA: {id.upper()}\n")
                    else:
                        with open(pt + '\\01_ComandoSQL.sql', 'a') as arquivo:
                            arquivo.write(f"INSERT INTO GedDocumento.Imagem VALUES ('{id.upper()}','{iddocumento.upper()}',1,'http://{uconta}.blob.core.windows.net/{cid.lower()}/{id.lower()}.{extensao.lower()}','{nome_arquivo}',NULL,{tamanho},GETDATE(),{idextensao[0]},'{user_resp.upper()}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);\n")
                           
                        with open(ptl + '\\logSucessoInsert.txt', 'a') as arquivo:
                           arquivo.write(f"DE: {nome_arquivo} | PARA: {id.upper()}\n")
                else:
                    
                    icone = '<i class="fa fa-file" aria-hidden="true" style="font-size:18px;color: gray;"></i>'
                    
                    comando = f"INSERT INTO GedSistema.Extensao (Extensao, Icone) VALUES ('{extensao.lower()}','{icone}');"
                    
                    insert_extensao(comando)
                    
                    id_nova_extensao = verifica_ext(extensao)
                        
                    with open(pt + '\\01_ComandoSQL.sql', 'a') as arquivo:
                        arquivo.write(f"INSERT INTO GedDocumento.Imagem VALUES ('{id.upper()}','{iddocumento.upper()}',1,'http://{uconta}.blob.core.windows.net/{cid.lower()}/{id.lower()}.{extensao.lower()}','{nome_arquivo}',NULL,{id_nova_extensao},'{user_resp.upper()}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);\n")
                        
                    with open(ptl + '\\logSucessoInsert.txt', 'a') as arquivo:
                        arquivo.write(f"DE: {nome_arquivo} | PARA: {id.upper()}\n")
                        
            # Nome final do arquivo
            destination_blob_name = f"{id.lower()}.{extensao.lower()}"
            



            try:
                # Arquivo de origem
                arquivo_de_origem = caminho
                
                # Copie o arquivo de origem do contêiner de origem para o contêiner de destino:
                #blob_client_destination.start_copy_from_url(arquivo_de_origem)

                # Crie um cliente para o compartilhamento de arquivos
                file_client = FileClient(account_name=uconta, account_key=usenha, share_name=f'http://{uconta}.blob.core.windows.net/{cid.lower()}')

                # Abra o arquivo para leitura
                with open("caminho_do_arquivo", "rb") as file:

                # Carregue o arquivo no compartilhamento de arquivos
                    file_client.upload_file(file.read(), "nome_do_arquivo")


                # #with open(caminho, 'rb') as arquivo_local:
                #     # Leia o arquivo em um buffer
                #     buffer = arquivo_local.read()
                #     # Grave o buffer no Azure Blob Storage
                #     blob_client.upload_blob(buffer, blob_name=destination_blob_name)
                #     # Feche o arquivo
                #     arquivo_local.close()
                
                with open (ptl + '\\LogSucessoAzure.txt', 'a') as arquivo:
                    arquivo.write(f"DE: {id.lower()}.{extensao.lower()} | PARA: {id}.{extensao.lower()}\n")
                    
            except Exception as e:
                with open (ptl + '\\LogErro.txt', 'a') as arquivo:
                    arquivo.write(f"Erro: {id} | Blob: {nome_arquivo} | {e}\n")
        
elif tp == 1:
    pt = input('\nDIGITE O CAMINHO PARA A PASTA DE TRABALHO: ')
    ptf, ptl = verificar_pasta(pt)
    
    user_resp = input('\nDIGITE O IDUSUARIO RESPONSÁVEL PELA ASSOCIAÇÃO: ')
    
    while verificar_usuario(user_resp) == False:
        print('\nIDUSUARIO INVÁLIDO!')
        user_resp = input('\nDIGITE O IDUSUARIO RESPONSÁVEL PELA ASSOCIAÇÃO: ')
        
    uco = input('\nDIGITE O IDUNIDADECLIENTE DE ORIGEM DOS ARQUIVOS: ')
    while buscar_dados_uc(uco) is None:
        print('\nIDUNIDADECLIENTE INVÁLIDO!')
        uco = input('\nDIGITE O IDUNIDADECLIENTE DE ORIGEM DOS ARQUIVOS: ')
        
    uido, ucontao, usenhao, cido = buscar_dados_uc(uco) 
    
    ucd = input('\nDIGITE O IDUNIDADECLIENTE DE DESTINO DOS ARQUIVOS: ')
    while buscar_dados_uc(ucd) is None:
        print('\nIDUNIDADECLIENTE INVÁLIDO!')
        ucd = input('\nDIGITE O IDUNIDADECLIENTE DE DESTINO DOS ARQUIVOS: ')
        
    uidd, ucontad, usenhad, cidd = buscar_dados_uc(ucd)   

    ccco = input('\nINSIRA A CADEIA DE CARACTERES DE CONSULTA DE ORIGEM: ') 
    cccd = input('\nINSIRA A CADEIA DE CARACTERES DE CONSULTA DE DESTINO: ')
    
    # Ler arquivo txt
    with open(pt + '\lista-img.txt', 'r') as arquivo: 

        # Conta o número total de linhas no arquivo
        total_linhas = sum(1 for linha in arquivo)

        # Reinicia o cursor do arquivo para o início
        arquivo.seek(0)
    
        for linha in tqdm(arquivo, total=total_linhas, desc='Progresso'):
            # Quebrando arquivo txt
            codigo, idimagem = linha.strip().split('|')
            
            # Buscando IdDocumento
            iddocumento = str(buscar_documento(codigo)[0])
            
            # Coletando dados do IdImagem
            idstatusocr, nome, qtdepagina, tamanho, idextensao, extensao = buscar_dados_imagem(idimagem)
            padrao = re.compile(re.escape(f".{extensao}"), re.IGNORECASE)
            nome = padrao.sub("", nome)
            nome = tratar_caract(nome)
            
            # Gerando Id para o arquivo
            id = str(new_id())
            
            # Verificando existência de arquivo
            existe_arquivo = verificar_arquivo(codigo,nome)
            
            if existe_arquivo:
                with open (ptl + '\\arquivo_ja_existentes.txt', 'a') as arquivo:
                    arquivo.write(f'O documento "{codigo}", já possui um arquivo com o nome da imagem id "{idimagem}" associado.\n') # Adicionar (num) nos arquivos existentes
                    
            else:
                with open (pt + '\\01_ComandoSQL.sql', 'a') as arquivo:
                    arquivo.write(f"INSERT INTO GedDocumento.Imagem VALUES ('{id.upper()}','{iddocumento.upper()}',{idstatusocr},'https://{ucontad}.blob.core.windows.net/{cidd.lower()}/{id.lower()}.{extensao.lower()}','{nome}',{qtdepagina},{tamanho},GETDATE(),{idextensao},'{user_resp}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);\n")
        
                with open (pt + '\\01_ComandoPS.bat', 'a') as arquivo:
                    arquivo.write(f".\\azcopy cp 'https://{ucontao}.blob.core.windows.net/{cido.lower()}/{idimagem.lower()}.{extensao.lower()}{ccco}' 'https://{ucontad}.blob.core.windows.net/{cidd.lower()}/{id.lower()}.{extensao.lower()}{cccd}' --recursive=true\n")
                    
                with open (ptl + '\\logSucesso.txt', 'a') as arquivo:
                    arquivo.write(f"DE: {idimagem.upper()} | PARA: {id.upper()}")
    
else:
    """
    pt = input('\nDIGITE O CAMINHO PARA A PASTA DE TRABALHO: ')
    ptf, ptl = verificar_pasta(pt)

    uco = input('\nDIGITE O IDUNIDADECLIENTE DE ORIGEM DOS ARQUIVOS: ')
    while buscar_dados_uc(uco) is None:
        print('\nIDUNIDADECLIENTE INVÁLIDO!')
        uco = input('\nDIGITE O IDUNIDADECLIENTE DE ORIGEM DOS ARQUIVOS: ')
        
    uid, uconta, usenha, cid = buscar_dados_uc(uco)
    
    ccco = input('\nDIGITE A CADEIA DE CARACTERES DE CONSULTA DE ORIGEM: ') 

    blobd = input('\nDIGITE A URL DA ASSINATURA DE ACESSO COMPARTILHADO DE DESTINO DOS ARQUIVOS: ')
    print("\n")
    
    with open(pt + '\lista-img.txt', 'r') as arquivo: 

        # Conta o número total de linhas no arquivo
        total_linhas = sum(1 for linha in arquivo)

        # Reinicia o cursor do arquivo para o início
        arquivo.seek(0)
    
        for linha in tqdm(arquivo, total=total_linhas, desc='Progresso'):
        
            # Quebrando arquivo txt
            codigo, idimagem = linha.strip().split('|')
            
            url1, url2 = blobd.split('?sv=')
            
            # Coletando dados do IdImagem
            idstatusocr, nome, qtdepagina, tamanho, idextensao, extensao = buscar_dados_imagem(idimagem)
            
            nome = f"{codigo}_{nome}"
            padrao = re.compile(re.escape(f".{extensao}"), re.IGNORECASE)
            nome = padrao.sub("", nome)
            nome = tratar_caract(nome)
            nome = tratar_url(nome)
            url = f"{url1}/{nome}.{extensao.lower()}?sv={url2}"
            
            with open(pt + '\\ComandoPS.bat', 'a') as arquivo:
                arquivo.write(f".\\azcopy cp 'https://{uconta}.blob.core.windows.net/{cid.lower()}/{idimagem.lower()}.{extensao.lower()}{ccco}' '{url}' --recursive=true\n")
                
            with open(ptl + '\\logSucesso.txt', 'a') as arquivo:
                arquivo.write(f"Comando para o Id '{idimagem}' criado com sucesso!\n")
    """
    pt = input('\nDIGITE O CAMINHO PARA A PASTA DE TRABALHO: ')
    ptf, ptl = verificar_pasta(pt)
    
    uco = input('\nDIGITE O IDUNIDADECLIENTE DE ORIGEM DOS ARQUIVOS: ')
    while buscar_dados_uc(uco) is None:
        print('\nIDUNIDADECLIENTE INVÁLIDO!')
        uco = input('\nDIGITE O IDUNIDADECLIENTE DE ORIGEM DOS ARQUIVOS: ')
        
    uido, ucontao, usenhao, cido = buscar_dados_uc(uco)
    
    account_name = ucontao
    account_key = usenhao
    source_container_name = cido.lower()
    
    ccco = input('\nINSIRA A CADEIA DE CARACTERES DE CONSULTA DE ORIGEM: ')
        
    cd = input('\nDIGITE O NOME DO CONTAINER DE DESTINO: ')
    while buscar_dados_uc(uco) is None:
        print('\nCONTAINER INVÁLIDO!')
        uco = input('\nDIGITE O NOME DO CONTAINER DE DESTINO: ')
        
    # Defina as informações de conexão para a conta de armazenamento do Azure de destino:
    destination_account_name = '***storagetmp'
    destination_account_key = '***'
    destination_container_name = cd.lower()
    
    print('\n')
        
    with open(pt + '\lista-img.txt', 'r') as arquivo: 

        # Conta o número total de linhas no arquivo
        total_linhas = sum(1 for linha in arquivo)

        # Reinicia o cursor do arquivo para o início
        arquivo.seek(0)
    
        for linha in tqdm(arquivo, total=total_linhas, desc='Progresso'):
        
            # Quebrando arquivo txt
            # codigo, idimagem = linha.strip().split('|')
            codigo, idimagem = linha.strip().split('|')
            
            # Coletando dados do IdImagem
            idstatusocr, nome, qtdepagina, tamanho, idextensao, extensao = buscar_dados_imagem(idimagem)
            
            source_blob_name = f"{idimagem.lower()}.{extensao.lower()}"
            
            nome = f"{codigo} - {nome}"
            padrao = re.compile(re.escape(f".{extensao}"), re.IGNORECASE)
            nome = padrao.sub("", nome)
            nome = tratar_caract(nome)
            
            # destination_blob_name = f"{nome}.{extensao.lower()}"
            
            destination_blob_name = f"{nome}.{extensao.lower()}"
            
            # Crie as instâncias dos objetos BlobServiceClient para cada conta:
            blob_service_source = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
            blob_service_destination = BlobServiceClient(account_url=f"https://{destination_account_name}.blob.core.windows.net", credential=destination_account_key)
            
            # Verifique se o arquivo já existe no contêiner de destino:
            blob_client_destination = blob_service_destination.get_blob_client(destination_container_name, destination_blob_name)
            
            # Verifique se já existe um blob com o mesmo nome no contêiner:
            if blob_client_destination.exists():
                with open (ptl + '\\LogErroExistente.txt', 'a') as arquivo:
                    arquivo.write(f"Arquivo '{nome}' já existente no destino | IdImagem: '{idimagem.upper()}'\n")
                
            else:
                try:
                    # Obtenha uma referência para o arquivo de origem no contêiner de origem:
                    source_blob_client = blob_service_source.get_blob_client(source_container_name, source_blob_name)
                    
                    # Concatenando o source_blob_client com a cadeia de caracteres de consulta de origem
                    source_blob_client = f"{source_blob_client.url}{ccco}"
                    
                    # Copie o arquivo de origem do contêiner de origem para o contêiner de destino:
                    blob_client_destination.start_copy_from_url(source_blob_client)
                    
                    with open (ptl + '\\LogSucesso.txt', 'a') as arquivo:
                        arquivo.write(f"DE: {idimagem.lower()}.{extensao.lower()} | PARA: {nome}.{extensao.lower()}\n")
                        
                except Exception as e:
                    with open (ptl + '\\LogErro.txt', 'a') as arquivo:
                        arquivo.write(f"Erro: {idimagem} | Blob: {source_blob_name}\n")

print('\nPROCESSO CONCLUÍDO!')