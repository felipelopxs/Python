# IMPORTANDO BIBLIOTECAS INTERNAS
from sql import UnidadeCliente


# IMPORTANDO BIBLIOTECAS DE TERCEIROS
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions, generate_container_sas, ContainerSasPermissions
import datetime
from typing import List

class ListarArquivos:
    def __init__(self,container:str,pasta:str)-> None:
        self.__listadearquivos = []
        self.__conta_tmp: str = "***storagetmp"
        self.__chave_tmp: str = "***"
        self.__listar = BlobServiceClient(account_url="{}.blob.core.windows.net".format(self.__conta_tmp), credential=self.__chave_tmp)
        containercliente = self.__listar.get_container_client(container)
        blobs = containercliente.list_blob_names()
        for blob in blobs:
            if blob.startswith(pasta) and 'METADADOS.xlsx' not in blob:
                self.__listadearquivos.append(blob.split('/')[2])

    @property
    def get_listadearquivos(self) -> List:
        return self.__listadearquivos


class CopiarArquivo:
    
    def __init__(self, id_imagem_com_extensao: str, nome_arquivo_com_extensao: str, id_unidade_cliente: str, pasta: str) -> None:
    
        self.__azure = UnidadeCliente(id_unidade_cliente)
        self.__dados_azure: dict = self.__azure.get_retorno
        
        self.__conta_tmp: str = "***storagetmp"
        self.__chave_tmp: str = "***"
    
        self.__origem = BlobServiceClient(account_url="{}.blob.core.windows.net".format(self.__dados_azure["azure_conta"]), credential=self.__dados_azure["azure_chave"])
        self.__destino = BlobServiceClient(account_url="{}.blob.core.windows.net".format(self.__conta_tmp), credential=self.__chave_tmp)
        
        __blob_origem = self.__origem.get_blob_client(self.__dados_azure["id_cliente"].lower(), id_imagem_com_extensao)
        __blob_client_destino = self.__destino.get_blob_client(self.__dados_azure["id_cliente"].lower(), "{}/Arquivos/{}".format(pasta, nome_arquivo_com_extensao))
        
        __sas = self.CriarSASToken(__blob_origem, self.__dados_azure["azure_chave"])
        
        __url_file = "{}?{}".format(__blob_origem.url, __sas)
        
        __blob_client_destino.start_copy_from_url(source_url=__url_file)

    def CriarSASToken(self, blob_client, account_key):
    
        start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=3)
        expiry_time = start_time + datetime.timedelta(days=1)
    
        sas_token = generate_blob_sas(
            account_name=blob_client.account_name,
            container_name=blob_client.container_name,
            blob_name=blob_client.blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=expiry_time,
            start=start_time
        )
    
        return sas_token
        
class UploadArquivo:

    def __init__(self, caminho_do_arquivo: str,id_unidade_cliente: str, pasta: str) -> None:
    
        self.__azure = UnidadeCliente(id_unidade_cliente)
        self.__dados_azure: dict = self.__azure.get_retorno
        
        self.__conta_tmp: str = "***storagetmp"
        self.__chave_tmp: str = "***"
    
        __blob_service_client = BlobServiceClient(account_url="https://{}.blob.core.windows.net".format(self.__conta_tmp), credential=self.__chave_tmp)
    
        self.__blob_client = __blob_service_client.get_blob_client(
            container=self.__dados_azure["id_cliente"].lower(),
            blob="{}/METADADOS.xlsx".format(pasta)
        )
        
        with open(caminho_do_arquivo, "rb") as f:
            data = f.read()
            self.__blob_client.upload_blob(data)
            
def GerarSASToken(container, pasta):
    
    blob_service_client = BlobServiceClient(account_url="***storagetmp.blob.core.windows.net", credential="***")
    
    container_client = blob_service_client.get_container_client(container)
    
    sas_permissions = ContainerSasPermissions(read=True, list=True, tag=True)
    
    start_time = datetime.datetime.now() - datetime.timedelta(hours=3)
    expiry_time = start_time + datetime.timedelta(days=31)
    
    # Gere o SAS token
    sas_token = generate_container_sas(
        container_client.account_name,
        container_client.container_name,
        account_key=container_client.credential.account_key,
        permission=sas_permissions,
        expiry=expiry_time,
        start=start_time
    )
    
    url_tmp: str = "https://***storagetmp.blob.core.windows.net/{}/{}?{}".format(container.lower(), pasta, sas_token)
    
    return url_tmp
    
def CalcularTamanho(container, pasta):
    
    blob_service_client = BlobServiceClient(account_url="***storagetmp.blob.core.windows.net", credential="***")
    
    container_name = container.lower()
    folder_name = "{}/Arquivos".format(pasta)
    
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs(name_starts_with=folder_name)
    
    total_tamanho_bytes = 0
    
    for blob in blob_list:
        total_tamanho_bytes += blob.size
    
    total_tamanho_gb = total_tamanho_bytes / (1024 ** 3)
    
    tamanho = "{:.2f}".format(total_tamanho_gb)
    
    return tamanho
    