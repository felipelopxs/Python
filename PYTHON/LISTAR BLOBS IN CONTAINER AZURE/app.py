from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def listar_blobs(nome_conta, chave_acesso, nome_container, nome_arquivo):
    try:
        # Criação da instância do cliente de serviço de blobs do Azure
        conta = "https://" + nome_conta + ".blob.core.windows.net/"
        blob_service_client = BlobServiceClient(account_url=conta, credential=chave_acesso)
        
        # Obter referência ao container
        container_client = blob_service_client.get_container_client(nome_container)
        
        # Listar blobs no container
        blobs = container_client.list_blobs()
        
        # Salvar os blobs em um arquivo de texto
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write("Blobs no container '{}':\n".format(nome_container))
            for blob in blobs:
                arquivo.write("\t{}\n".format(blob.name))
    
        print("Lista de blobs salva em '{}'".format(nome_arquivo))
    
    except Exception as e:
        print("Erro:", str(e))

if __name__ == "__main__":
    # Informações da conta do Azure
    nome_conta_azure = "***storagetmp"
    chave_acesso = "***********"
    nome_container = "********************"
    
    # Nome do arquivo onde a lista será salva
    nome_arquivo = r"caminho"
    
    # Chama a função para listar os blobs e salvar no arquivo
    listar_blobs(nome_conta_azure, chave_acesso, nome_container, nome_arquivo)

