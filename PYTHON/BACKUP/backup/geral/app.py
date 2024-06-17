# IMPORTANDO BIBLIOTECAS INTERNAS
from logo import Logo
from sql import Backup, UnidadeCliente
from data import DataHora
from base64_loc import decode
from azure_loc import CopiarArquivo, UploadArquivo, GerarSASToken, CalcularTamanho, ListarArquivos
from validador import ValidadorDePasta, RemoverPasta, RemoverArquivo, LimparTela
from constantes import BASE64_MANUAL



# IMPORTAÇÕES DE BIBLIOTECAS DE TERCEIROS
from tqdm import tqdm
import os



# FUNÇÕES
def obter_where(pasta_de_trabalho) -> str:
    selecao = None

    while selecao not in [0, 1]:
        selecao: int = int(input("[0] BACKUP COMPLETO | [1] BACKUP PARCIAL: "))

        if selecao == 0:
            where_dados: str = ""
        elif selecao == 1:
            with open(pasta_de_trabalho + "\\WHERE.txt", "r", encoding="utf-8") as where:
                where_dados: str = where.read()
        else:
            print("A opção selecionada é inválida, tente novamente.")

    return where_dados

def incluir_imagens() -> bool:
    selecao = None
    
    while selecao not in [0, 1]:
        selecao: int = int(input("[0] INCLUIR IMAGENS | [1] NÃO INCLUIR IMAGENS: "))

        if selecao == 0:
            selecao = True
        elif selecao == 1:
            selecao = False
        else:
            print("A opção selecionada é inválida, tente novamente.")

    return selecao

# APLICAÇÃO
LimparTela()

id_unidade_cliente: str = input("DIGITE O IdUnidadeCliente DE ORIGEM: ")
unidade_cliente = UnidadeCliente(id_unidade_cliente)
dados_unidade_cliente = unidade_cliente.get_retorno

pasta_de_trabalho: str = input("INFORME SUA PASTA DE TRABALHO: ")

where_dados: str = obter_where(pasta_de_trabalho)
inclusao_de_imagens: bool = incluir_imagens()
data_hora = DataHora()

LimparTela()

ValidadorDePasta("{}\\Metadados".format(pasta_de_trabalho))
ValidadorDePasta("{}\\Log".format(pasta_de_trabalho))
ValidadorDePasta("{}\\Comandos".format(pasta_de_trabalho))
ValidadorDePasta("{}\\Chamado".format(pasta_de_trabalho))

consulta_de_backup = Backup(dados_unidade_cliente["id_cliente"], where_dados, inclusao_de_imagens)

if inclusao_de_imagens == True:
    lista_de_arquivos = consulta_de_backup.get_dados_anexos
    total_de_arquivos: int = len(lista_de_arquivos)

caminho_para_salvar = os.path.join(pasta_de_trabalho, "Metadados")
consulta_de_backup.salvar_planilha(caminho=caminho_para_salvar)

# try:
#     UploadArquivo("{}\\{}\\METADADOS.xlsx".format(pasta_de_trabalho, data_hora), id_unidade_cliente, data_hora)

#     with open(pasta_de_trabalho + "\\Log\\LOG_DE_SUCESSO.txt".format(id_unidade_cliente, data_hora), "a", encoding="utf-8") as log_de_sucesso_md:
#         log_de_sucesso_md.write("Backup do arquivo 'METADADOS.xlsx' realizado com sucesso.\n")

# except Exception as erro_metadados:
#     with open(pasta_de_trabalho + "\\Log\\LOG_DE_INSUCESSO.txt".format(id_unidade_cliente, data_hora), "a", encoding="utf-8") as log_de_insucesso_md:
#         log_de_insucesso_md.write("Erro ao realizar o backup do arquivo 'METADADOS.xlsx' | {}\n".format(erro_metadados))
  
# RemoverPasta("{}\\{}".format(pasta_de_trabalho, data_hora))

decode(BASE64_MANUAL, "{}\\Chamado\\Processo Download Azure.pdf".format(pasta_de_trabalho))
sas_token: str = GerarSASToken(dados_unidade_cliente["id_cliente"], data_hora)

with open(pasta_de_trabalho + "\\Chamado\\BACKUP DADOS COMPLETOS.txt", "a", encoding="utf-8") as arquivo_azcopy:
    arquivo_azcopy.write(".\\azcopy cp '{}' 'C:\\Backup' --recursive=true;\n".format(sas_token))

if inclusao_de_imagens == True:
    listadearquivos = ListarArquivos(dados_unidade_cliente["id_cliente"].lower(), data_hora).get_listadearquivos

    print("\nREALIZANDO BACKUP DOS ARQUIVOS.")
    for arquivo in tqdm(lista_de_arquivos, total=total_de_arquivos, desc="PROGRESSO"):

        nome_arquivo, id_imagem = arquivo.split("|@#")
        
        try:
            if nome_arquivo not in listadearquivos:

                CopiarArquivo(id_imagem, nome_arquivo, id_unidade_cliente, data_hora)
                
                with open(pasta_de_trabalho + "\\Log\\LOG_DE_SUCESSO.txt".format(id_unidade_cliente, data_hora), "a", encoding="utf-8") as log_de_sucesso:
                    log_de_sucesso.write("Backup do arquivo '{}' realizado com sucesso.\n".format(id_imagem))
                    
                with open(pasta_de_trabalho + "\\Comandos\\{}_{}_ARQUIVOS_PARA_DELETAR_AZURE.txt".format(id_unidade_cliente, data_hora), "a", encoding="utf-8") as exclusao_azure:
                    exclusao_azure.write("{}\n".format(id_imagem))
                    
                with open(pasta_de_trabalho + "\\Comandos\\{}_{}_DELETE_DEFINITIVO.sql".format(id_unidade_cliente, data_hora), "a", encoding="utf-8") as comando_sql:
                    comando_sql.write("DELETE FROM GedDocumento.Imagem WHERE Id = '{}';\n".format(id_imagem.split('.')[0].upper()))

            else:
                with open(pasta_de_trabalho + "\\Log\\LOG_DE_INSUCESSO.txt".format(id_unidade_cliente, data_hora), "a", encoding="utf-8") as log_de_insucesso:
                    log_de_insucesso.write("Arquivo já existente no container '{}' \n".format(id_imagem))

        except Exception as erro_copia:
            
            erro_copiar_arquivo = str(erro_copia).replace("\n", " ")
            
            with open(pasta_de_trabalho + "\\Log\\LOG_DE_INSUCESSO.txt".format(id_unidade_cliente, data_hora), "a", encoding="utf-8") as log_de_insucesso:
                log_de_insucesso.write("Erro ao copiar o arquivo '{}' | {}\n".format(id_imagem, erro_copiar_arquivo))
        
    tamanho = CalcularTamanho(dados_unidade_cliente["id_cliente"], data_hora)

    with open(pasta_de_trabalho + "\\Chamado\\MENSAGEM_PADRAO.txt", "a", encoding="utf-8") as mensagem_padrao:
        mensagem_padrao.write(
            """Prezados(as),

                Foi realizado o backup registros solicitados,
                para realização do download serão necessários {} GB disponíveis na máquina que realizará o download.

                Os arquivos ficaram disponíveis para download por um período de 30 dias.

                À disposição.""".format(tamanho)
        )

print("\nPROCESSO CONCLUÍDO.\n")
